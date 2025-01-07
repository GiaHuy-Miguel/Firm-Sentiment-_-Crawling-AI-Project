# CREATING FIRM SENTIMENT INDEX FROM NEWS ARTICLES' TITLE WITH SELENIUM AND PHOBERT 
## *** IN ORDER TO RUN THIS PROJECT, PLEASE INSTALL SELENIUM, PANDAS, AS WELL AS OTHER USED LIBRARIES AND CLONE THIS RESPRITORY: https://huggingface.co/mr4/phobert-base-vi-sentiment-analysis (DANG VIET DUNG, 2023)***
# MECHANISM: 
This project uses selenium to crawl articles from CafeF.com - a well known newspaper that delivers information specifically related to firms and stock market. After that, crawled articles ared fed nto an AI Model (PhoBERT) in order to retrieve its sentiment.
# CODE PREVIEW: 
```python

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
YEAR_STOP = 2015
YEAR_START = 2024
COMPANY_FILE = 'COMPANY.xlsx'
CSV_FILE = 'OUTPUT_2.csv'

#  OPTIMIZATION
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")

# Retrieve list of firms from Excel 
df = pd.read_excel(COMPANY_FILE)
list_companies = df['company'].tolist()
# list_companies = ['ccl']

# Create an csv file
csv_file = WriteCsv(CSV_FILE)
csv_file.create()

# Loop through each firm in the list 
driver = webdriver.Chrome(options=chrome_options)
for company in list_companies:
    driver.get(f"https://cafef.vn/du-lieu/tin-doanh-nghiep/{company}/event.chn")
    while True: # A while loop is used to make Selenium only crawl titles from the needed period
        try: 
            # Retrieve articles from the opening page
            articles_src = wait(driver, 9999, By.XPATH, '//*[@id="divEvents"]')
            articles = articles_src.find_elements(By.TAG_NAME, "li")
        
            if len(articles) == 0: # Break the while loop if there is no article (Handling blank page)
                break
            # Get time stamps and titles
            for article in articles:
                # Lấy time_stamp
                time_stamp = wait(article, 9999, By.TAG_NAME, "span").text
                year = int(time_stamp[6:10])
                
                # Only collect titles within the needed period
                if year < YEAR_STOP:
                    break  # Stop processing if year is before the needed period

                if year < YEAR_START: # Stop processing if year is after the needed period
                # Lấy title báo
                    title = article.find_element(By.TAG_NAME, "a").get_attribute("title")
                    arr = [time_stamp, company, title]
                    # Feed to model
                    model = Model("mr4/phobert-base-vi-sentiment-analysis",arr)
                    result= model.load_model()
                    
                    # Append to csv
                    csv_file.write(result)
            
            # Load next page
            driver.find_element(By.XPATH, '//*[@id="spanNext"]').click()
            time.sleep(0.5) #Wait for next page to looad
        except Exception as e:
                print(f"An error occurred while processing {company}: {e}")
                break 
driver.quit()

```
# SYSTEM DESIGN: 
This project has 2 system designs (called versions) with its own pros and cons, based on hardware or Internet condition and the website status. 
However, I reccomend to use the veriosn 2 (the lastest version) due to higher stability and modification. These systems can be explained by the graph belowed: 
## SYSTEM EXPLICATION GRAPH
![image](https://github.com/user-attachments/assets/869bd73b-d515-49f2-8279-3e0d29f50c5e)

# CREDIT: 
[mr4/phobert-base-vi-sentiment-analysis](https://huggingface.co/mr4/phobert-base-vi-sentiment-analysis) (Dang Viet Dung, 2023)
[PhoBERT: Pre-trained language models for Vietnamese](https://aclanthology.org/2020.findings-emnlp.92/) (Nguyen & Tuan Nguyen, Findings 2020)

# CONTACT: 
## FURTHER INQUIRY AND SUPPORT PLEASE CONTACT: giahuynguyentruong2004@gmail.com 

# THANK YOU!
