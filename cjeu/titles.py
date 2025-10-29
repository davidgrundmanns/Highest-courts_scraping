# import base python packages
import time
import glob
import os

# import installed packages
## for scraping
### Pyderman
import pyderman as driver
path = driver.install(browser=driver.chrome)
#print('Installed geckodriver driver to path: %s' % path)
### Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
## for datamanagement
### Pandas
import pandas as pd

# requires a vector of celex numbers used to identify cases (= 'celex_nos')
celex_nos = celex_nos.values.tolist()

# start webdriver: Chrome
serv = Service(driver.install(browser=driver.chrome))
opts = webdriver.ChromeOptions()
#opts.add_argument("--incognito")
#opts.add_argument("headless") # run driver without poping browser
opts.add_experimental_option("detach", True)

# set chrome settings
profile = {"plugins.always_open_pdf_externally": True, # Disable Chrome's PDF Viewer
               "download.default_directory":  "G:\Meine Ablage\13. Projects\scrape-cjeu" , "download.extensions_to_open": "applications/pdf"}
opts.add_experimental_option("prefs", profile)

web = webdriver.Chrome(service = serv, options = opts)

for celex in celex_nos:
    link = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A"+str(celex)[2:-2]
    web.get(link)
    web.implicitly_wait(5)

    # extract date
    title = web.find_element(By.XPATH, ".//p[@id='title']").text
    titles.append(title)

titlesdata = pd.DataFrame({'celex':celex_nos,
                     'title':titles})

titlesdata.to_csv('titlesdata.csv', sep = ";", encoding='utf-8-sig')
