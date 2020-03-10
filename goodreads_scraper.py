from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime
import csv

# For each review, store at least the following (not a complete list):

#     edition title
#     edition language
#     review text
#     review language
#     review author
#     review author sex (gender) HOW???
#     review rating

# as many other metadata as you can extract from GoodReads?
# <a class="actionLinkLite loadingLink" rel="nofollow" data-keep-on-success="true" data-remote="true" href="#" onclick="new Ajax.Request('/book/reviews/40718205-the-dinner?rating=5&amp;amp;text_only=true', {asynchronous:true, evalScripts:true, method:'get', parameters:'authenticity_token=' + encodeURIComponent('wk0apYk4YJDnGPqsc23DrY71W0wike8TXvbXLp3UGfVi8iMF5vvGUzwOw9bf2VGzv5DELxlhzifHVA5HzNQH1g==')}); return false;" style="display: inline;">5 stars <span class="greyText">(12062)</span></a>
# /book/reviews/40718205-the-dinner?rating=5&amp;amp;text_only=true

# <select name="language_code" id="language_code"><option value="">All Languages</option><option value="af">Afrikaans ‎(1)</option>
# <option value="az">Azərbaycan dili ‎(1)</option>
# <option value="id">Bahasa Indonesia ‎(16)</option>
# <option value="ca">Català ‎(1)</option>
# <option value="da">Dansk ‎(2)</option>
# <option value="de">Deutsch ‎(20)</option>
# <option value="et">Eesti ‎(7)</option>
# <option value="en">English ‎(14647)</option>
# <option value="es">Español ‎(134)</option>
# <option value="fr">Français ‎(22)</option>
# <option value="it">Italiano ‎(85)</option>
# <option value="lv">Latviešu valoda ‎(17)</option>
# <option value="lt">Lietuvių kalba ‎(11)</option>
# <option value="hu">Magyar ‎(3)</option>
# <option selected="selected" value="nl">Nederlands ‎(370)</option>
# <option value="no">Norsk ‎(1)</option>
# <option value="pl">Polski ‎(4)</option>
# <option value="pt">Português ‎(33)</option>
# <option value="ru">Pусский язык ‎(21)</option>
# <option value="ro">Română ‎(12)</option>
# <option value="sk">Slovenčina ‎(1)</option>
# <option value="sl">Slovenščina ‎(3)</option>
# <option value="fi">Suomi ‎(17)</option>
# <option value="sv">Svenska ‎(4)</option>
# <option value="vi">Tiếng Việt ‎(1)</option>
# <option value="tr">Türkçe ‎(8)</option>
# <option value="hr">hrvatski ‎(2)</option>
# <option value="is">Íslenska ‎(3)</option>
# <option value="cs">česky, čeština ‎(3)</option>
# <option value="el">Ελληνικά ‎(24)</option>
# <option value="bg">български език ‎(55)</option>
# <option value="mk">македонски јазик ‎(1)</option>
# <option value="uk">українська ‎(2)</option>
# <option value="he">עברית ‎(5)</option>
# <option value="ar">العربية ‎(85)</option>
# <option value="fa">فارسی ‎(2)</option>
# <option value="th">ไทย ‎(1)</option>
# <option value="ka">ქართული ‎(4)</option></select>


# editions
# https://www.goodreads.com/work/editions/6463092-het-diner

#de reviews lijken niet te veranderen bij een andere editie

edition_url='https://www.goodreads.com/book/show/40718205-the-dinner'
review_language='it'

def scrape_page(review_language):

    title='The dinner'
    filename='dinner'
    edition_language='eng' # dit lijkt geen variabele in de reviews

    review_id=''
    author=''
    author_gender=''
    rating=''
    scraped_folder='scraped_dinner'
    counter=0
    reviews=driver.find_elements_by_class_name('friendReviews ')
    
    for review in reviews:
        content=review.find_elements_by_css_selector("[id^='freeText']")
        review_id=review.find_element_by_class_name('review').get_attribute("id")
        review_date=review.find_element_by_class_name('reviewDate').text
        review_date=review_date.strip(",") #remove ,
        
        try:
            author=review.find_element_by_css_selector("[class='user']").text
            # author=author.encode("utf-8")
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
        print('---------------------------------------------------------------------------')

        if len(content) > 1:
            #there is a hidden part that forms the complete text. Is the second element
            text=content[1].get_attribute('textContent')
        else:
            #if there is no 'more' link, all the text is in the first element
            text=content[0].text

        #rating stars:
        # did not like is= 1, it was ok =2 , liked it =3, really liked it =4, it was amazing =5
        
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

        counter+=1




driver = webdriver.Firefox(executable_path=r'geckodriver\geckodriver.exe')
driver.get(edition_url)

for x in range(0, 10):
    time.sleep(3)
    ddelement= Select(driver.find_element_by_id('language_code'))
    ddelement.select_by_value(review_language)

    time.sleep(4)

    scrape_page(review_language)

    try:
        next_button=driver.find_element_by_class_name('next_page')
        next_button.click()
    except:
        print('no next button')
        break