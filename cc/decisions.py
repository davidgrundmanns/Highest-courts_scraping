# download dir
download_dir = "\\download\\fr"

# Link structure; change start and end date as needed
#link = "https://recherche.conseil-constitutionnel.fr/?mid=a35262a4dccb2f69a36693ec74e69d26&filtres[]=type_doc%3AdossierComplet&offsetCooc=&offsetDisplay=0&nbResultDisplay=10&nbCoocDisplay=&UseCluster=&cluster=&showExtr=&sortBy=date&typeQuery=3&dateBefore=&dateAfter=&xtmc=&xtnp=p1&rech_ok=1&date-from=2000-01-01&date-to=2021-12-31&filtres1[]=sous_type_decision:%22DC-loi%22&filtres1[]=sous_type_decision:%22DC-LO%22&filtres1[]=sous_type_decision:%22DC-traite%22&filtres1[]=sous_type_decision:%22DC-reglement%22&filtres1[]=sous_type_decision:%22QPC%22"

# two prepared decision filters for QPC (priority preliminary ruling on the issue of constitutiontality) 
# and DC (conformity decisions - control of constitutionality of ordinary and organic laws, treaties, 
# parliament regulations)


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

# start webdriver: Chrome
serv = Service(driver.install(browser=driver.chrome))
opts = webdriver.ChromeOptions()
#opts.add_argument("--incognito")
#opts.add_argument("headless") # run driver without poping browser
opts.add_experimental_option("detach", True)

profile = {"plugins.always_open_pdf_externally": True, # Disable Chrome's PDF Viewer
               "download.default_directory":  "\\downl\\qpc" , "download.extensions_to_open": "applications/pdf"}
opts.add_experimental_option("prefs", profile)

web = webdriver.Chrome(service = serv, options = opts)

# Access webdriver and open page
# qpc decisions (starting Jan 1st, 2010 to Dec 31st, 2024)
# web.get("https://recherche.conseil-constitutionnel.fr/?mid=a35262a4dccb2f69a36693ec74e69d26&filtres[]=type_doc%3AdossierComplet&offsetCooc=&offsetDisplay=0&nbResultDisplay=10&nbCoocDisplay=&UseCluster=&cluster=&showExtr=&sortBy=date&typeQuery=3&dateBefore=&dateAfter=&xtmc=&xtnp=p1&rech_ok=1&date-from=2010-01-01&date-to=2024-12-31&filtres1[]=sous_type_decision:%22QPC%22") # open browser
# DC decisions (starting Jan 1st, 2010 to Dec 31st, 2024)
web.get("https://recherche.conseil-constitutionnel.fr/?mid=a35262a4dccb2f69a36693ec74e69d26&filtres[]=type_doc%3AdossierComplet&offsetCooc=&offsetDisplay=0&nbResultDisplay=10&nbCoocDisplay=&UseCluster=&cluster=&showExtr=&sortBy=date&typeQuery=3&dateBefore=&dateAfter=&xtmc=&xtnp=p1&rech_ok=1&date-from=2010-01-01&date-to=2024-12-31&filtres1[]=sous_type_decision:%22DC-loi%22&filtres1[]=sous_type_decision:%22DC-LO%22&filtres1[]=sous_type_decision:%22DC-traite%22&filtres1[]=sous_type_decision:%22DC-reglement%22") # open browser
pages = web.find_element(By.XPATH, ".//nav[@class='pager']/ul/li/span").text # find page number
pages = pages.split(" ")[1] # split text that contains page number

links = [] # create empty list to hold links
# for every i (page) in the range of 1 to int(pages) = 126
for i in range(1, int(pages)+1):
    elements = web.find_elements(By.XPATH, ".//div[@class='title']/a") # find each decision links in decision titles
    # for every link in list of webelements, do...7
    for element in elements:
        links.append(element.get_attribute("href")) # append link to list of links
    if(i < int(pages)):
        nextpg = web.find_element(By.XPATH, ".//a[@rel='next']")
        web.execute_script("arguments[0].click();", nextpg)

# save old cwd and change to new one
oldwd = os.getcwd() # save current working directory
os.chdir(download_dir) # change working directory to download directory

# create objects to store information from following loop
titles = []
subtitles = []
dectypes = []
description_ruling = []
description_case = []


# for every link in list of links, get the pdf link
for link in links:
    web.get(link) # open the link
    time.sleep(1)

    # save title
    titles.append(web.find_element(By.XPATH, ".//h1[@class='title']").text)

    # save subtitle
    subtitles.append(web.find_element(By.XPATH, ".//div[@class='right']/div[1]").text)

    # save decision type
    dectypes.append(web.find_element(By.XPATH, ".//div[@class='right']/div[2]").text)

    # save description + decision (either together or split, as you wish)
    if len(web.find_elements(By. XPATH, ".//div[@class='wrapper-content']/div[1]/blockquote")) == 1:
        description_ruling.append(web.find_element(By.XPATH, ".//div[@class='wrapper-content']/div[1]/blockquote").text)
    else:
        if len(web.find_elements(By. XPATH, ".//div[@class='wrapper-content']/div[1]/div[1]/blockquote")) == 1:
            description_ruling.append(web.find_element(By.XPATH, ".//div[@class='wrapper-content']/div[1]/div[1]/blockquote").text)
        else:
            if len(web.find_elements(By. XPATH, ".//div[@class='wrapper-content']/div[1]/div[1]/div[1]/blockquote")) == 1:
                description_ruling.append(web.find_element(By.XPATH, ".//div[@class='wrapper-content']/div[1]/div[1]/div[1]/blockquote").text)
            else:
                description_ruling.append(str("NA"))
    # if it doesnt exist look one div deeper
    # and one div deeper
    description_case.append(web.find_element(By.XPATH, ".//div[@class='wrapper-content']/div[1]").text)

    # download decision
    pdf_url = web.find_element(By.XPATH, ".//a[@class='lien-version-pdf']").get_attribute("href") # get the pdf download link of the decision
    web.get(pdf_url) # open the decision pdf (to download)
    # while there is a partial file, wait...
    while(glob.glob("*.crdownload")!=[]):
        time.sleep(1)
    time.sleep(1) # wait one second
    # download government observation
    if len(web.find_elements(By.XPATH, ".//a[contains(@data-smarttag, 'observations_du_gouvernement')]")) == 1:
        obs_gov = web.find_element(By.XPATH, ".//a[contains(@data-smarttag, 'observations_du_gouvernement')]").get_attribute("href")
        web.get(obs_gov)
    else:
        time.sleep(1)
    # download contributions exterior
    if len(web.find_elements(By.XPATH, ".//a[contains(@data-smarttag, 'contributions_exterieures')]")) == 1:
        contr_ext = web.find_element(By.XPATH, ".//a[contains(@data-smarttag, 'contributions_exterieures')]").get_attribute("href")
        web.get(contr_ext)
    else:
        time.sleep(1)
    # download saisine par senateurs
    if len(web.find_elements(By.XPATH, ".//a[contains(@data-smarttag, 'senateurs')]")) == 1:
        saisine_sen = web.find_element(By.XPATH, ".//a[contains(@data-smarttag, 'senateurs')]").get_attribute("href")
        web.get(saisine_sen)
    else:
        time.sleep(1)
     # download saisine par deputes
    if len(web.find_elements(By.XPATH, ".//a[contains(@data-smarttag, 'deputes')]")) == 1:
        saisine_dep = web.find_element(By.XPATH, ".//a[contains(@data-smarttag, 'deputes')]").get_attribute("href")
        web.get(saisine_dep)
    else:
        time.sleep(1)
print("Finished loop")

# change working directory to project main directory
os.chdir(oldwd)

data = pd.DataFrame(
    {'title':titles,
     'subtitle':subtitles,
     'decision_type':dectypes,
     'link':links}
)

# split title string in decision number, proceeding type (QPC oder DC), Date
data['decnumber'] = [myname.split(" ")[2].strip() for myname in data['title']]
# strip() removes leading and trailing white space

# proceeding type
#data['title'].split(" ")[3] # rewrite as list comprehension as above
data['proctype'] = [myname.split(" ")[3].strip() for myname in data['title']]
# date
#data['title'].split(" du ")[1] # rewrite as list comprehension as above
data['date'] = [myname.split(" du ")[1].strip() for myname in data['title']]
# save DataFrame
data.to_csv('dataframe.csv', sep = ";", encoding='utf-8-sig')
