'''
Configuration.
'''

# for the editions list scrape, the editions URL of Goodreads. After this scrape, the created list will be iterated to scrape each edition
ALL_EDITIONS_URL = 'https://www.goodreads.com/work/editions/4640799-harry-potter-and-the-philosopher-s-stone' # 'https://www.goodreads.com/work/editions/6463092-het-diner'

# prefix of how the CSV's and XML's will be named
TITLE ='The_philosophers_stone'

#specify the languages of the editions that must be scraped, in the name format of goodreads as in the created editions_csv
EDITION_LANGUAGES=['English', 'Dutch', 'Spanish', 'French', 'German'] 
EDITIONS_CSV = TITLE + '_editions_goodreads.csv' # No particular need to change this.