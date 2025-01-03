import time
import random as rd
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
YEAR = 2015

#  OPTIMIZATION
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")

# LIST CÁC DOANH NGHIỆP
df = pd.read_excel('COMPANY.xlsx')
list_companies = df['company'].tolist()

# # LIST CÁC TIÊU ĐỀ
list_titles = []

# Duyệt qua list các doanh nghiệp
driver = webdriver.Chrome(options=chrome_options)
for company in list_companies:
    #print(company)
    driver.get(f"https://cafef.vn/du-lieu/tin-doanh-nghiep/{company}/event.chn")
    
    #Điều kiện vòng while Lấy trong 
    flag = True 
    while flag: 
        # Lấy list các element chứa title
        articles_src = WebDriverWait(driver, timeout=120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="divEvents"]')))
        # articles_src = driver.find_element(By.XPATH, '//*[@id="divEvents"]') 
        articles = articles_src.find_elements(By.TAG_NAME, "li")
        if len(articles) == 0: 
            break
        # Duyệt qua từng element trong list và lấy title + timestamp
        for article in articles:
            # Lấy time_stamp
            time_stamp = article.find_element(By.TAG_NAME, "span").text
            year = int(time_stamp[6:10])

            # Nếu year là 2017 đổ xuống thì break vòng for và hủy vòng while
            if year == 2024:
                continue
            elif year < YEAR:
                flag = False
                break
            # Lấy title báo
            title = article.find_element(By.TAG_NAME, "a").get_attribute("title")
            arr = [time_stamp, title]
            list_titles.append(arr)
            print(arr)

        #Bấm nút load trang tiếp theo 
        driver.find_element(By.XPATH, '//*[@id="spanNext"]').click()
        time.sleep(rd.randint(1,2)) #Đợi để load trang tiếp theo 
driver.quit()