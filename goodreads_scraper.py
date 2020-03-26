from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import csv
import os.path
from os import path
from config import *

###########################################################################################################
# This script scrapes all the languages in the Goodreads selectbox, and will scrape the 5 - 1 star ratings. Also it will scrape 'this edition'.
# The star ratings are scraped for 'this edition'. But this seems not to work really well, as a lot of ratings are showing the text 'review of another edition'
# so the only reviews that are certain applicable for this edition are the ones marked with scrape_type: 'edition'
# Data are stored in a csv file. Data are appended if the review id is not yet in the general csv of scraped reviews.
# for each review an xml file is made and stored in the folder for the edition.
# for every edition a new csv file is created, as it can hold thousands of reviews. A general CSV stores al the review id's 
# and is used to check if a review already was stored, to prevent double reviews. 
###########################################################################################################

# For each review, store at least the following (not a complete list):
#     edition title
#     edition language
#     review text
#     review language
#     review author
#     review author sex (gender) HOW? not implemented yet
#     review rating

# as many other metadata as you can extract from GoodReads?


def read_editions_csv(filename):
    try:
        with open(filename , newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = list(reader)
            return data
    except IOError:
        return []



def make_xml_file(filename, title, review_date, review_language, review_id, author, rating, text, edition, edition_language, scrape_type):
    scraped_folder='XML/' + filename

    if not path.exists(scraped_folder): 
        os.mkdir(scraped_folder)
        
        # try:
        #     os.mkdir(scraped_folder)
        #     print("Directory " , scraped_folder ,  " Created ") 
        # except FileExistsError:
        #     print("Directory " , scraped_folder,  " already exists")
    text=text.replace("&", "&amp;")

    xml="<scrape>"
    xml+="<title>" + title +"</title>"
    xml+="<edition>" + edition +"</edition>"
    xml+="<edition_language>" + edition_language +"</edition_language>"
    xml+="<review_language>" + review_language +"</review_language>"
    xml+="<scrape_type>" + scrape_type +"</scrape_type>"
    xml+="<review_date>" + review_date +"</review_date>"
    xml+="<review_id>" + review_id + "</review_id>"
    xml+="<author>" + author +  "</author>"
    xml+="<rating>" + rating + "</rating>"
    xml+="<text>" + text + "</text>"
    xml+="</scrape>"

    try: 
        f = open(scraped_folder+"/" + review_id + "_" + filename +"_" + review_language +".xml",  "w", encoding="utf-8")
        f.write(xml)
        f.close()
    except:
        print (filename)
        print ('kon geen bestand opslaan')



def make_csv_file(title, review_date, review_language, review_id, author, rating, text, filename, edition_language, scrape_type):
    
    if not path.exists('CSV/' + filename + '_scrapes_goodreads.csv'):
        write_header=True
    else:
        write_header=False

    with open('CSV/' + filename + '_scrapes_goodreads.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['review_id', 'title', 'review_date', 'review_language', 'edition_language','scrape_type', 'author', 'rating', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
            print('csv created with header')
        writer.writerow({'review_id': review_id,'title':title, 'review_date':review_date, \
        'review_language': review_language, 'edition_language':edition_language, 'scrape_type':scrape_type, 'author': author, 'rating':rating, 'text':text})
    
    #csv for checking if review already was scraped 
    with open('check_all_scrapes/all_scrapes_goodreads.csv', 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['review_id', 'title', 'filename', 'scrape_type']
        writer2 = csv.DictWriter(f, fieldnames=fieldnames)
        writer2.writerow({'review_id': review_id,'title':title, 'filename': filename, 'scrape_type': scrape_type})
        
        
  
def read_csv_file():
    with open('check_all_scrapes/all_scrapes_goodreads.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
        return data



def scrape_page(driver, review_language, filename, title, edition, edition_language, scrape_type):

    review_id=''
    author=''
    rating=''
    counter=0

    time.sleep(1)
    reviews=driver.find_elements_by_class_name('friendReviews')

    for review in reviews:
       
        # read the csv with reviews that are already done, 
        try:
            existing_reviews=read_csv_file()
        except:
            existing_reviews=[]
        
        content=review.find_elements_by_css_selector("[id^='freeText']")
        review_id=review.find_element_by_class_name('review').get_attribute("id")
        split= review_id.split("_")
        review_id=split[1]

        review_date=review.find_element_by_class_name('reviewDate').text
        review_date=review_date.strip(",")
        
        try:
            author=review.find_element_by_css_selector("[class='user']").text
        except:
            author='unknown'
            print('no author found')
        
        try:
            rating=review.find_element_by_class_name("staticStars").text
        except:
            rating='unknown'
            print('no stars found')

        print(review_id)
        print(review_date)
        print(author.encode("utf-8"))
        print(rating)
       
        try:
            if len(content) > 1:
                #there is a hidden part that forms the complete text. Is the second element
                text=content[1].get_attribute('textContent')
            else:
                #if there is no 'more' link, all the text is in the first element
                text=content[0].text
        except:
            text='could not scrape'


        text = text.replace('\r','\n')# replace line breaks that cause trouble 
        
        #rating stars:
        # did not like is= 1, it was ok =2 , liked it =3, really liked it =4, it was amazing =5
        review_exists=False

        for existing_review in existing_reviews:
            if review_id == existing_review[0] and scrape_type == existing_review[3] :
                review_exists=True
                print('Review already in csv, id = ' + review_id)
                break

        if review_exists == False and text != 'could not scrape': # in some editions there are many ratings without text
            make_csv_file(title, review_date, review_language, review_id, author, rating, text, filename, edition_language, scrape_type)
            make_xml_file(filename, title, review_date, review_language, review_id, author, rating, text, edition, edition_language, scrape_type)
            print('Created new line in csv, created xml file')

        counter+=1

        print('-------------------------------')
        


def scrape_loop(driver, review_language, filename, more_position, edition, edition_language, scrape_type):

    time.sleep(2)
    ddelement= Select(driver.find_element_by_id('language_code'))
    ddelement.select_by_value(review_language)


    if more_position != '': 
        time.sleep(3)
        filters = driver.find_element_by_css_selector("a[id^='span_class_gr-hyperlink_more_filters_']")
        hover = ActionChains(driver).move_to_element(filters)
        hover.perform() # this is a weak spot: the hovering not always works, what is the problem? 
        time.sleep(2)
        tooltip=driver.find_element_by_class_name("tooltip")
        stars_links=tooltip.find_elements_by_class_name("loadingLink")
        time.sleep(2)
        print('must be 10, otherwise element not found: ', len(stars_links))

        # first click position 7; this edition,
        driver.execute_script("arguments[0].click();", stars_links[7]) # click with javascript, as the element ccould be hidden
        time.sleep(1)
        # driver.execute_script("arguments[0].click();", stars_links[9]) # click text only. But this is not working, as it now shows reviews from other editions as well
        # time.sleep(1)

        if more_position < 7:
            # list more filter, on 0=all, 1= 5 stars, 2 = 4stars, 3 = 3 stars, 4 = 2 stars, 5 = 1 star, 6 = editions all, 7 = this edition, 8 = content any, 9 = text-only
            driver.execute_script("arguments[0].click();", stars_links[more_position]) # click with javascript, as the element ccould be hidden


    for x in range(0, 10):
        time.sleep(4)

        scrape_page(driver, review_language, filename, title, edition, edition_language, scrape_type)

        try:
            next_button=driver.find_element_by_class_name('next_page')
            next_button.click()
        except:
            print('no next button')
            break



#functions for scraping on edition, language and star-ratings

def edition_scrape(filename, edition_url, edition, edition_language):
    scrape_type='edition'
    more_position=7 # integer, is position of the 'this edition' selection
    review_language='' # empty for all, must be all to get selection pane with the 'edition' option
    driver = webdriver.Firefox(executable_path=r'geckodriver\geckodriver.exe')
    driver.get(edition_url)
    scrape_loop(driver, review_language, filename, more_position, edition, edition_language, scrape_type)
    driver.close()


def language_scrape(filename, edition_url, edition, edition_language):
    scrape_type='language'
    languages=['az','id','ca','da','de','et', 'en', 'es', 'fr', 'it','lv','lt', 'hu', 'nl', 'no', 'pl', 'pt', 'ru', 'ro', 'sk','sl','fi', \
    'sv', 'vi', 'tr', 'hr', 'is','cs', 'el', 'bg', 'mk', 'uk','he', 'ar', 'fa', 'th', 'ka']
    more_position='' # empty so the scraper will choose the language selection part
    driver = webdriver.Firefox(executable_path=r'geckodriver\geckodriver.exe')
    driver.get(edition_url)
    for review_language in languages:
        print('####################################')
        print('language = ' + review_language)
        scrape_loop(driver, review_language, filename, more_position, edition, edition_language, scrape_type)
    driver.close()


def stars_scrape(filename, edition_url, edition, edition_language):
    scrape_type= 'stars'

    # more_position: 1 =5 stars, 2 =4 stars, 3=3 stars, 4 =2 stars, 5 =1 star
    # a lot of errors here: element not found, caused by slow internet connection? Seems random problem, seems every 3 time elements are not found.
    for more_position in range(1, 6):
        #needs fresh driver for new round. 
        print('#####################################################')
        stars_number = 6 - more_position
        print('Number of stars: ', stars_number)
        driver = webdriver.Firefox(executable_path=r'geckodriver\geckodriver.exe')
        driver.get(edition_url)
        review_language='' # must be empty, select on rating works only with all langugaes
        scrape_loop(driver, review_language, filename, more_position, edition, edition_language, scrape_type)
        driver.close() # for each round a new driver is started, to secure the starsrating-pane is available



#choose edition to scrape
title=TITLE #from config, for in the csv and XML files

# change this to get a new edition from the list with editions
edition_from_list=24 #Todo, as script extension

editions=read_editions_csv( EDITIONS_CSV ) # from config.py
edition_languages=['English', 'Dutch', 'Spanish', 'French', 'German']
editions_req_languages=[]

for edition in editions:
    if edition[5] in edition_languages:
        #print(edition)
        editions_req_languages.append(edition) # TODO loop this one to scrape everything at once


if __name__ == "__main__":

    edition_url=editions_req_languages[edition_from_list][0] # this will be retrieved from the list of scraped editions itterating through the csv 
    edition_language=editions_req_languages[edition_from_list][5] 
    edition_split=edition_url.split( '/')
    edition=edition_split[5]
    title=title.replace(" ", "_")
    filename=title + "_" + edition # naming the csv file

    # do functions:
    edition_scrape(filename, edition_url, edition, edition_language) # This one results in fresh reviews every time

    # language_scrape(filename, edition_url, edition, edition_language) # this is fairly independent of edition, as it overlaps all editions. Run only one time seems sufficient

    # stars_scrape( filename, edition_url, edition, edition_language) # about the same, most of the ratings are taken from outher editions, although 'this edition' was selected.

