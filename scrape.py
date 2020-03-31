from scripts import goodreads_scraper
from scripts import editions_goodreads_scraper
import sys
from config import *

title=TITLE #config
editions= goodreads_scraper.read_editions_csv( EDITIONS_CSV ) # config
edition_languages=EDITION_LANGUAGES #config

def scrape_loop(title, editions, edition_from_list, loop):
    end = 0
    counter = 0

    if loop and edition_from_list=='all':
        end = len(editions) + 1

    elif loop and type(edition_from_list).__name__ == 'int':
        counter=edition_from_list -1
        end = len(editions)

    # scrape only specified row
    else:
        counter = edition_from_list -1 
        end = counter + 1

    for page in range(counter, end):
        edition_url=editions[counter][0] # itterating through the csv 
        edition_language=editions[counter][5] 
        edition_split=edition_url.split( '/')
        edition=edition_split[5]
        title=title.replace(" ", "_")
        filename=title + "_" + edition # naming the csv file
        print('processing row: ', counter +1,  'of ',len(editions))
        
        if edition_language in edition_languages: # if the language in column 5 is in the list of languages
            goodreads_scraper.edition_scrape(filename, edition_url, edition, edition_language ) # This one results in fresh reviews every time
            print('scraping...')
        else:
            print('skipping, language not in specified list.')
        counter+=1
         
        if counter==len(editions):
            print('scraping done!')



# scrape.py, with args:
# - makelist (To be done first. To create an editions CSV with all the editions, and their individual urls that need to be scraped)
# - edition [number] (scrapes the edition of a book on a certain row of the editions CSV, ie.'scrape.py edition 12', scrapes the edition at row 12, row 1 is '1', not '0')
# - edition all (scrapes the whole list in a loop, starting from te first row. This will almost certainly grind to a halt with a long editions CSV, as the pushing of buttons with celenium is error prone)
# - edition start [number] (will scrape in a loop from a specified row in the selected languages list, to be used when an error has occurred and the scraping needs to be started again.)
# - language (will scrape on all review languages. But the reviews will target different editions, and if scraped are excluded from scraping again, so possibly not useful when reviews per edition are the research focus.) 
# - stars (will scrape per star rating. Will target all editions and overlap the edition scrapes, so possibly not useful if the focus is on reviews per edition)

def main():
    if  sys.argv[1:][0]=='makelist':
        editions_goodreads_scraper.scrape_loop()

    if sys.argv[1:][0]=='language':
        filename=title + '_language_scrape'
        edition_language='all'
        edition_url=editions[0][0] # first edition in editions csv
        edition_split=edition_url.split( '/')
        edition=edition_split[5]
        goodreads_scraper.language_scrape(filename, edition_url, edition, edition_language)

    if sys.argv[1:][0]=='stars':
        filename=title + '_stars_scrape'
        edition_language='all'
        edition_url=editions[0][0] # first edition in editions csv
        edition_split=edition_url.split( '/')
        edition=edition_split[5]
        goodreads_scraper.stars_scrape(filename, edition_url, edition, edition_language)

    if sys.argv[1:][0]=='edition' and sys.argv[1:][1] != 'all' and sys.argv[1:][1] != 'start' :
        loop=False
        edition_from_list = int(sys.argv[1:][1])
        scrape_loop(title, editions, edition_from_list, loop)

    if sys.argv[1:][0]=='edition' and sys.argv[1:][1] == 'all':
        edition_from_list = 'all'
        loop=True
        scrape_loop(title, editions, edition_from_list, loop)

    if sys.argv[1:][0]=='edition' and sys.argv[1:][1] == 'start':
        loop=True
        edition_from_list = int(sys.argv[1:][2])
        scrape_loop(title, editions, edition_from_list, loop)
    


if __name__ == "__main__":
    main()