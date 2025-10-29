# import base python packages
import time
import glob
import os

# import installed packages
## for scraping
### Pyderman
import pyderman as driver
path = driver.install(browser=driver.chrome)
### Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
## for datamanagement
### Pandas
import pandas as pd
import openpyxl

# Read the Excel file containing decision URLs
df = pd.read_excel("G:\\Meine Ablage\\13. Projects\\scrape_hcj_amici\\input\\hcj_cases.xlsx")
links = df['url'].tolist()

# start webdriver
web = webdriver.Chrome()
web.maximize_window()

# objects to store results
briefs_header = list()
briefs_filer = list()
decision_links = list()

# start loop over links
for i in range(0, len(links)):
    # Access webdriver and open page
    web.get(links[i]) # open browser
    time.sleep(1)
    # find amici by keyword "friend" (hebrew: ידידי)
    if len(web.find_elements(By.XPATH, '//tbody[.//tr/td/p/span[contains(text(),"ידיד")]]')) == 1:
        entry = web.find_elements(By.XPATH, '//tbody[.//tr/td/p/span[contains(text(),"ידיד")]]')
        # the first entry is where we need to look
        for j in range(0, len(entry)):
            decision_links.append(links[i])
            briefs_filer.append(entry[j].text)
        print(str(i) + " successful")
    else:
        print(str(i) + " no entry found")

data = pd.DataFrame(
    {'link':decision_links,
     'filer':briefs_filer}
)

# save DataFrame
data.to_csv('dataframe.csv', sep = ";", encoding='utf-8-sig')
