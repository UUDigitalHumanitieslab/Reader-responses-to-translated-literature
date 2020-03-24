import goodreads_scraper
import editions_goodreads_scraper
import sys
from config import *


title=TITLE #from config
editions= goodreads_scraper.read_editions_csv( EDITIONS_CSV ) # from config.py
edition_languages=['English', 'Dutch', 'Spanish', 'French', 'German'] #TODO to config
editions_req_languages=[]

# get only the relevant editions from the csv and make new list
for edition in editions:
    if edition[5] in edition_languages:
        #print(edition)
        editions_req_languages.append(edition)


def scrape_loop(title, editions_req_languages, edition_from_list):
    end = 0
    counter = 0

    # if an edition row number is passed, scrape only this row. If no int is passed, but a string, loop through all the rows of the csv.
    if type(edition_from_list).__name__ == 'int':
        counter = edition_from_list
        end = counter + 1
    else: 
        end = len(editions_req_languages) + 1

    for page in range(counter, end):
        edition_url=editions_req_languages[counter][0] # itterating through the csv 
        edition_language=editions_req_languages[counter][5] 
        edition_split=edition_url.split( '/')
        edition=edition_split[5]
        title=title.replace(" ", "_")
        filename=title + "_" + edition # naming the csv file
        
        # method
        goodreads_scraper.edition_scrape(edition_url, edition, edition_language ) # This one results in fresh reviews every time
        counter+=1
         


def main():
    if  sys.argv[1:][0]=='makelist': # create the list of editions of a title with an url defined in the config
        editions_goodreads_scraper.scrape_loop()
    if sys.argv[1:][0]=='edition' and sys.argv[1:][1] != 'all':
        edition_from_list = int(sys.argv[1:][1]) # i.e. arguments: edition 2 = the 2e row in the csv editions file, passed as int
        scrape_loop(title, editions_req_languages, edition_from_list)
    if sys.argv[1:][0]=='edition' and sys.argv[1:][1] == 'all':
        edition_from_list = 'all'
        scrape_loop(title, editions_req_languages, edition_from_list)


if __name__ == "__main__":
    main()