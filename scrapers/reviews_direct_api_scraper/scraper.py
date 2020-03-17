import sys
from edition_scraper.edition_utils import get_editions
from reviews_direct_api_scraper.parser import parse_html
from reviews_direct_api_scraper.collector import collect
from review_utils.review_export_utils import Exporter, get_new_reviews 


def scrape(edition_csv_path, edition_languages, output_path):
    '''
    Parameters:
        edition_csv_path -- path to the csv containing the scraped editions
        edition_languages -- specify the languages to include when collecting editions.
            Example: ['English', 'Dutch', 'German', 'Spanish', 'French']
            All other languages will be ignored
        output_path -- a full path (incl. filename and extension) where you expect the output.
    '''
    fieldnames = ['review_id', 'edition_id', 'review_date', 'review_language', 'author', 'rating', 'text']
    exporter = Exporter()
    editions = get_editions(edition_csv_path, edition_languages)
    
    for e in editions:
        reviews = collect_for_edition(e)
        new_reviews = get_new_reviews(output_path, reviews)
        exporter.to_csv(output_path, fieldnames, new_reviews)


def collect_for_edition(edition):
    '''
    Collect all reviews for an edition.
    '''
    print('collecting reviews for edition {}'.format(edition.get_edition_id()))
            
    reviews = []    
    for i in range(1, 6):
        reviews.extend(collect(edition, True, i, True))
        
    print("All reviews collected for {}".format(edition.get_edition_id()))
    return reviews
