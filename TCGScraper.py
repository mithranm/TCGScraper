import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium.webdriver.support.ui import Select
#from parse import parse ----we did not use it instead went with Regular expression
   
driver = webdriver.Chrome('C:/chromedriver.exe')
site_url = 'https://www.tcgplayer.com'
driver.get(site_url)
time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'lxml')
i = 1
Top100products = []
attr = 'dropdown-link-' + str(i)
atag = str(soup.find('a', {'id': attr}))
string_pattern = r'href="/[a-zA-Z0-9/?=&;]*'
regex_pattern = re.compile(string_pattern)
productgrid_url = re.findall(regex_pattern, atag)
productgrid_url[0] = str(productgrid_url[0]).replace('href="', '')
driver.get(site_url + productgrid_url[0])
time.sleep(2)
selectCtrl = Select(driver.find_element_by_xpath('//*[@id="app"]/div/section[2]/section/div/div[2]/div/div/div[2]/div/select'))
selectCtrl.select_by_value('best-selling')
j = 0
numcards = 100
while j < numcards:
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    products = [s.text for s in soup.findAll('span', {'class': 'search-result__title'})]
    i = 0
    for product in products:
        driver2 = webdriver.Chrome('C:/chromedriver.exe')
        attr = 'search-result__image--' + str(i)
        atag = str(soup.find('a', {'data-testid': attr}))
        string_pattern = '/product/\d*/'
        regex_pattern = re.compile(string_pattern)
        product_url = re.findall(regex_pattern, atag)
        driver2.get(site_url + product_url[0])
        time.sleep(1)
        soup2 = BeautifulSoup(driver2.page_source, 'lxml')
        productprice = soup2.find('span', {'class': 'spotlight__price'}).text
        Top100products.append(str(product) + ',' + str(productprice))
        print(Top100products[j])
        driver2.close()
        i += 1
        j += 1
        if j >= numcards:
            break
    if j < numcards:
        driver.find_element_by_id('nextButton').click()
     
df = pd.DataFrame(Top100products)
df.to_csv('C:/Users/mithr/Desktop/buggysenchou.csv', sep='\t', encoding='utf-8');
driver.quit()