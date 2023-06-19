import config
from bs4 import BeautifulSoup
import selenium as se
from selenium import webdriver
import time

def getSoup(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options)
    browser.implicitly_wait(3)
    browser.get(url)
    time.sleep(3)
    return BeautifulSoup(browser.page_source, "lxml")

def getNumPages():
    soup = getSoup(config.POL_URL)
    pages = int(soup.select(".q-pagination b:nth-child(2)")[0].text)
    print("Pages:",str(pages))
    return pages