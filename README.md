# FIRM SENTIMENT PROJECT 
## This project uses Selenium to crawl titles from articles about firm on CafeF.com and PhoBERT to give out sentiment prediction
***To use run project, please install Pytorch, Pandas, Selenium and clone this respitory beforehand: https://huggingface.co/mr4/phobert-base-vi-sentiment-analysis***

# CODE PREVIEW: 
```
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

# LIST OF FIRMS
df = pd.read_excel(COMPANY_FILE)
list_companies = df['company'].tolist()
# list_companies = ['ccl']

# CSV FILE
csv_file = WriteCsv(CSV_FILE)
csv_file.create()

# LOOP THROUGH LIST OF FIRMS
driver = webdriver.Chrome(options=chrome_options)
for company in list_companies:
    #print(company)
    driver.get(f"https://cafef.vn/du-lieu/tin-doanh-nghiep/{company}/event.chn")

    while True: # Continuously looping for one company until meet conditions
        try: 
            # Get list of articles
            articles_src = wait(driver, 1000, By.XPATH, '//*[@id="divEvents"]')
            articles = articles_src.find_elements(By.TAG_NAME, "li")
        
            if not articles:  # No more articles then break
                    break
            # Loop through each article and get title & timestamp
            for article in articles:

                # Retrieve time_stamp
                time_stamp = wait(article, 1000, By.TAG_NAME, "span").text
                year = int(time_stamp[6:10])
                
                # Only fetch data from required time
                if year < YEAR:
                    break  # Stop processing if year is before threshold

                if year != 2024: #skip year 2024
                # Retrive title 
                    title = article.find_element(By.TAG_NAME, "a").get_attribute("title")
                    arr = [time_stamp, company, title]
                    
                    # Run model
                    model = Model("mr4/phobert-base-vi-sentiment-analysis",arr)
                    result= model.load_model()
                    
                    # Write csv
                    csv_file.write(result) 
            
            # Load nextpage
            driver.find_element(By.XPATH, '//*[@id="spanNext"]').click()
            time.sleep(0.5) # Wait for next page to load
        except Exception as e:
                print(f"An error occurred while processing {company}: {e}")
                break 
driver.quit()
```

# CREDIT: 
[mr4/phobert-base-vi-sentiment-analysis](https://huggingface.co/mr4/phobert-base-vi-sentiment-analysis) (Dang Viet Dung, 2023) 

[PhoBERT: Pre-trained language models for Vietnamese](https://aclanthology.org/2020.findings-emnlp.92/) (Nguyen & Tuan Nguyen, Findings 2020)
