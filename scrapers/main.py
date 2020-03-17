import sys
from reviews_direct_api_scraper import scraper

'''
This is an example of a script consuming a scraper.
Use something like this to access the scraper(s).
'''

# EDITIONS_PATH = '/home/alexhebing/Projects/Reader-responses-to-translated-literature/scrapers/editions/the_Dinner_editions_goodreads.csv'
EDITIONS_PATH = '/home/alexhebing/Projects/Reader-responses-to-translated-literature/scrapers/edition_scraper/test_editions.csv'
OUTPUT_PATH = '/home/alexhebing/Projects/Reader-responses-to-translated-literature/scrapers/test_out.csv'
LANGUAGES = ['English', 'Dutch', 'German', 'Spanish', 'French']


def main(args):
    scraper.scrape(EDITIONS_PATH, LANGUAGES, OUTPUT_PATH)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
