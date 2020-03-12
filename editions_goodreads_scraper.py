from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import csv



#########################################
# Scrapes the list of editions of a title, and stores the urls and other important infromatiom per edition.
# To create a new CSV, change the variable 'scraped_title' and the url tot the list of editions of a work, and specify the number of editions (to be found at the top of the page)
# be patient: the browser closes and starts up again after a few seconds.

# the Dinner: https://www.goodreads.com/work/editions/6463092-het-diner' 137 
# Harry Potter and the Sorcerer's Stone : https://www.goodreads.com/work/editions/4640799-harry-potter-and-the-philosopher-s-stone 751

########################################

scraped_title='Harry_Potter_phil_stone'
# url='https://www.goodreads.com/work/editions/6463092-het-diner'
url='https://www.goodreads.com/work/editions/4640799-harry-potter-and-the-philosopher-s-stone'

number_editions=751


def make_csv_file(title, published, edition_information, author, ISBN, edition_language, average_rating):
    print(title + "," + published + "," + edition_information )
    print(author + "," + ISBN + "," + edition_language + "," + average_rating)
    
    with open(scraped_title + '_editions_goodreads.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'published', 'edition_information', 'author', 'ISBN', 'edition_language', 'average_rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'title': title, 'published': published, 'edition_information':edition_information, 'author':author, 'ISBN': ISBN, 'edition_language': edition_language, 'average_rating':average_rating })



def scrape_page(driver ):

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
            # print(dataTitles[counter].text)
            # print(dataValue.text)
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




number_pages= int(round( (number_editions / 30) + 0.4999, 0))
print(number_pages)



for page in range(1, number_pages+1):
    
    url_page=url+'?page='+ str(page)

    driver = webdriver.Firefox(executable_path=r'geckodriver\geckodriver.exe')
    driver.get(url_page)
    time.sleep(2)
    scrape_page(driver)
    driver.close()



