import time
import pandas as pd
from model import Model
from csv_write import WriteCsv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait for element to exist
def wait(element, timeout, by, source):
    return WebDriverWait(element, timeout=timeout).until(EC.presence_of_element_located((by, source)))

# CONFIGURATION
YEAR = 2015
COMPANY_FILE = 'COMPANY.xlsx'
CSV_FILE = 'OUTPUT_2.csv'

#  OPTIMIZATION
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")

# LIST CÁC DOANH NGHIỆP
df = pd.read_excel(COMPANY_FILE)
list_companies = df['company'].tolist()
# list_companies = ['ccl']

#File CSV
csv_file = WriteCsv(CSV_FILE)
csv_file.create()

# Duyệt qua list các doanh nghiệp
driver = webdriver.Chrome(options=chrome_options)
for company in list_companies:
    #print(company)
    driver.get(f"https://cafef.vn/du-lieu/tin-doanh-nghiep/{company}/event.chn")
    
    #Điều kiện vòng while Lấy trong 
    while True: 
        try: 
            # Lấy list các element chứa title
            articles_src = wait(driver, 1000, By.XPATH, '//*[@id="divEvents"]')
            articles = articles_src.find_elements(By.TAG_NAME, "li")
        
            if not articles:  # No more articles then break
                    break
            # Duyệt qua từng element trong list và lấy title + timestamp
            for article in articles:

                # Lấy time_stamp
                time_stamp = wait(article, 1000, By.TAG_NAME, "span").text
                year = int(time_stamp[6:10])
                
                # Lấy trong khoảng thời gian cần lấy 
                if year < YEAR:
                    break  # Stop processing if year is before threshold

                if year != 2024: #skip year 2024
                # Lấy title báo
                    title = article.find_element(By.TAG_NAME, "a").get_attribute("title")
                    arr = [time_stamp, company, title]
                    
                    # chạy model
                    model = Model("mr4/phobert-base-vi-sentiment-analysis",arr)
                    result= model.load_model()
                    
                    # Viết csv
                    csv_file.write(result)
            
            # Bấm nút load trang tiếp theo 
            driver.find_element(By.XPATH, '//*[@id="spanNext"]').click()
            time.sleep(0.5) #Đợi để load trang tiếp theo 
        except Exception as e:
                print(f"An error occurred while processing {company}: {e}")
                break 
driver.quit()