from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import csv

###########################################################################################################
# This script scrapes all the languages in the Goodreads selectbox, and will scrape the 5 - 1 star ratings. 
# Data are stored in a csv file. Dat are appended if the review id is not yet in the csv
# for each review an xml file is made and stored in the folder as specified in 'scraped_folder' variable.
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



def make_xml_file(scraped_folder, filename, title, review_date, review_language, review_id, author, rating, text):

    xml="<scrape><title>" + title +"</title>"
    xml+="<review_date>" + review_date +"</review_date>"
    xml+="<review_language>" + review_language +"</review_language>"
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



def make_csv_file(title, review_date, review_language, review_id, author, rating, text, filename):
    
    with open(filename + '_scrapes_goodreads.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['review_id', 'title', 'review_date', 'review_language', 'author', 'rating', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'review_id': review_id,'title':title, 'review_date':review_date, \
        'review_language': review_language, 'author': author, 'rating':rating, 'text':text})


def read_csv_file(filename):

    with open(filename + '_scrapes_goodreads.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
        return data



def scrape_page(driver, review_language, filename, title):

    #edition_language='eng' # will be retrieved from the editions scraper
    review_id=''
    author=''
    # author_gender=''
    rating=''
    scraped_folder='scraped_dinner'
    counter=0
    reviews=driver.find_elements_by_class_name('friendReviews')

   
    for review in reviews:

        # read the csv with reviews that are already done, 
        try:
            existing_reviews=read_csv_file(filename)
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
       
        if len(content) > 1:
            #there is a hidden part that forms the complete text. Is the second element
            text=content[1].get_attribute('textContent')
        else:
            #if there is no 'more' link, all the text is in the first element
            text=content[0].text

        #rating stars:
        # did not like is= 1, it was ok =2 , liked it =3, really liked it =4, it was amazing =5
        review_exists=False

        for existing_review in existing_reviews:
            if review_id == existing_review[0]:
                review_exists=True
                print('Review already in csv, id = ' + review_id)
                break

        if review_exists == False:
            make_csv_file(title, review_date, review_language, review_id, author, rating, text, filename)
            make_xml_file(scraped_folder, filename, title, review_date, review_language, review_id, author, rating, text)
            print('Created new line in csv, created xml file')

        counter+=1

        print('-------------------------------')
        


def scrape_loop(driver, review_language, more_position):

    time.sleep(2)
    ddelement= Select(driver.find_element_by_id('language_code'))
    ddelement.select_by_value(review_language)

    if more_position != '': 
        time.sleep(2)

        filters = driver.find_element_by_css_selector("a[id^='span_class_gr-hyperlink_more_filters_']")
        hover = ActionChains(driver).move_to_element(filters)
        hover.perform()

        tooltip=driver.find_element_by_class_name("tooltip")
        stars_links=tooltip.find_elements_by_class_name("loadingLink")
        time.sleep(4)
        print(len(stars_links))

        # list more filter, on 0=all, 1= 5 stars, 2 = 4stars, 3 = 3 stars, 4 = 2 stars, 5 = 1 star, 6 = editions all, 7 = this edition, 8 = content any, 9 = text-only
        driver.execute_script("arguments[0].click();", stars_links[more_position]) # click with javascript, as the element ccould be hidden



    for x in range(0, 10):
        time.sleep(3)

        scrape_page(driver, review_language, filename, title)

        try:
            next_button=driver.find_element_by_class_name('next_page')
            next_button.click()
        except:
            print('no next button')
            break







filename='dinner'
title='The dinner'

edition_url='https://www.goodreads.com/book/show/40718205-the-dinner' # this will be retrieve from the list of scraped editions itterating through the csv

languages=['az','id','ca','da','de','et', 'en', 'es', 'fr', 'it','lv','lt', 'hu', 'nl', 'no', 'pl', 'pt', 'ru', 'ro', 'sk','sl','fi', \
    'sv', 'vi', 'tr', 'hr', 'is','cs', 'el', 'bg', 'mk', 'uk','he', 'ar', 'fa', 'th', 'ka']

more_position=''

# looping and scraping the languages
# driver = webdriver.Firefox(executable_path=r'geckodriver\geckodriver.exe')
# driver.get(edition_url)

# for review_language in languages:
#     print('####################################')
#     print('language = ' + review_language)

#     scrape_loop(driver, review_language, more_position)


# driver.close()


def scrape():
    # scraping reviews based on rating
    for more_position in range(1, 6):
        #needs fresh driver for new round
        print('#####################################################')
        print(more_position)
        
        driver = webdriver.Firefox(executable_path=r'geckodriver\geckodriver.exe')
        driver.get(edition_url)

        #more_position=5 # 1=5 stars, 2 =4 stars, 3=3 stars, 4 =2 stars, 5 =1 star
        review_language='' # must be empty, select on rating works only with all langugaes

        scrape_loop(driver,review_language, more_position)
        driver.close()



#scrape_loop(driver,review_language, more_position)
