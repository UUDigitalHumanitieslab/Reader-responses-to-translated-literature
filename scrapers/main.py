import sys
from reviews_web_scraper import scraper

'''
This is an example of how to call a scraper now that they are in modules
'''


def main(args):
    scraper.scrape()
    
if __name__ == '__main__':
    sys.exit(main(sys.argv))
