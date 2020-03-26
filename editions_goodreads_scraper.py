from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import csv
from config import *

#########################################
# Scrapes the list of editions of a title, and stores the urls and other important information per edition in a CSV.
# To create a new CSV, in 'config.py' change the variable 'title' and the url on ALL_EDITIONS_URL, and run script.
########################################


def read_csv_file(scraped_title):
    with open(scraped_title + '_editions_goodreads.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
        return data


def make_csv_file(title, published, edition_information, author, ISBN, edition_language, average_rating):
    print(title + "," + published + "," + edition_information )
    #print(author + "," + ISBN + "," + edition_language + "," + average_rating)
    
    with open(scraped_title + '_editions_goodreads.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'published', 'edition_information', 'author', 'ISBN', 'edition_language', 'average_rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        #read the csv with editions that are already scraped
        existing_editions=read_csv_file(scraped_title)
     
        title_exists = False

        for existing_edition in existing_editions:
           if title == existing_edition[0]:
               title_exists= True
               print('title already in CSV')
               break

        if title_exists == False:
            writer.writerow({'title': title, 'published': published, 'edition_information':edition_information, 'author':author, 'ISBN': ISBN, 'edition_language': edition_language, 'average_rating':average_rating })
            print('line written to CSV')



def scrape_page(driver):

    title=''
    published=''
    edition_information=''
    author=''
    ISBN=''
    edition_language=''
    average_rating=''

    contents=driver.find_elements_by_class_name("editionData")

    for content in contents:
        dataRows=content.find_elements_by_class_name("dataRow")
        title=content.find_element_by_xpath(".//a").get_attribute("href") # get the link, not the title itself
        published=dataRows[1].text
        edition_information=dataRows[2].text
        details_link=content.find_element_by_class_name("detailsLink")
        details_link.click()
        more_details=content.find_element_by_class_name("moreDetails")
        dataTitles=more_details.find_elements_by_class_name("dataTitle")
        dataValues=more_details.find_elements_by_class_name("dataValue")

        counter=0
        for dataValue in dataValues:
            if dataTitles[counter].text == 'Author(s):':
                author=dataValue.text
            if dataTitles[counter].text == 'ISBN:' or dataTitles[counter].text == 'ISBN13:':
                ISBN=dataValue.text
            if dataTitles[counter].text == 'Edition language:':
                edition_language=dataValue.text
            if dataTitles[counter].text == 'Average rating:':
                average_rating=dataValue.text
            
            counter+=1
            
        make_csv_file(title, published, edition_information, author, ISBN, edition_language, average_rating)
    return len(contents) # how many editions were found on page



def scrape_loop():
    # a new screen is triggered and closed every loop, to avoid the @#$ overlay that invites to log in, and that obscures the buttons
    results_number=30 #number of results of a full page
    page=1
    while results_number > 29:
        url_page=url+'?page='+ str(page)
        driver = webdriver.Firefox(executable_path=r'geckodriver\geckodriver.exe')
        driver.get(url_page)
        time.sleep(2)
        results_number=scrape_page(driver)
        page+=1
        if results_number > 29:
            print( 'Please wait for another page to appear...')
        else:
            print ('Done with scraping.')
        driver.close()


scraped_title=TITLE # config.py
url= ALL_EDITIONS_URL # config.py

if __name__ == "__main__":
    #print('Number of pages to be scraped : ', number_pages)
    scrape_loop()
    	
