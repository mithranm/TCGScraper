import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium.webdriver.support.ui import Select

#Set these constants
sortoption = 'best-selling'
numcards = 100
webdriverpath = 'C:/chromedriver.exe'
cardgame = 0 #set this from 1-6 to choose different games

#Creates a new driver and navigates to the site
driver = webdriver.Chrome(webdriverpath)
site_url = 'https://www.tcgplayer.com'
driver.get(site_url)
time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'lxml')
topproducts = []

#Finds the a tag with dropdown link in the page
attr = 'dropdown-link-' + str(cardgame)
atag = str(soup.find('a', {'id': attr}))

#Finds the link to product search from that a tag
string_pattern = 'href="/[a-zA-Z0-9/?=&;]*'
regex_pattern = re.compile(string_pattern)
productgrid_url = re.findall(regex_pattern, atag)

#Remove href from the string found so that it is the url
productgrid_url[0] = str(productgrid_url[0]).replace('href="', '')
driver.get(site_url + productgrid_url[0])
time.sleep(2)

#Select the sort option using the Selenium support ui library
selectCtrl = Select(driver.find_element_by_xpath('//*[@id="app"]/div/section[2]/section/div/div[2]/div/div/div[2]/div/select'))
selectCtrl.select_by_value(sortoption)

#Loop through all the cards on the page and then go to the next one until we hit numcards
j = 0
while j < numcards:
    time.sleep(1)
    #Make new soup and then find every "search-result"
    soup = BeautifulSoup(driver.page_source, 'lxml')
    products = [s.text for s in soup.findAll('span', {'class': 'search-result__title'})]
    
    #Loop through every card
    i = 0
    for product in products:
        #New driver that goes to each card's page so we don't lose our place in the search page
        driver2 = webdriver.Chrome(webdriverpath)
        
        #This regex looks for the a tag containing product id and then isolates it 
        attr = 'search-result__image--' + str(i)
        atag = str(soup.find('a', {'data-testid': attr}))
        string_pattern = '/product/\d*/'
        regex_pattern = re.compile(string_pattern)
        product_url = re.findall(regex_pattern, atag)
        
        #Driver nagivates there and then puts the spotlight price inside an array
        driver2.get(site_url + product_url[0])
        time.sleep(1)
        soup2 = BeautifulSoup(driver2.page_source, 'lxml')
        productprice = soup2.find('span', {'class': 'spotlight__price'}).text
        topproducts.append(str(product) + ',' + str(productprice))
        print(topproducts[j])
        driver2.close()
        i += 1
        j += 1
        if j >= numcards:
            break
    if j < numcards:
        driver.find_element_by_id('nextButton').click()

#Outputs the scraped data to a csv file in the desktop
df = pd.DataFrame(topproducts)
df.to_csv('C:/Users/mithr/Desktop/TCGScraped.csv', sep='\t', encoding='utf-8');
driver.quit()