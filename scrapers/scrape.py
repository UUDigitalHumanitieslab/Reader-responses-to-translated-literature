import os
import sys
import argparse
from edition_scraper import scraper as editions_scraper
from review_scraper import scraper as review_scraper
from utilities.utils import log

EDITION_LANGUAGES = ['English', 'German', 'Dutch', 'French', 'Spanish']


def main(sys_args):
    args = parse_arguments(sys_args)
    if args.edition_languages == 'all':
        edition_languages = EDITION_LANGUAGES
    else:
        edition_languages = args.edition_languages
        if not isinstance(args.edition_languages, list):
            edition_languages = [args.edition_languages]

    editions = editions_scraper.scrape(
        args.editions_url, args.editions_export_path)
    review_scraper.scrape(editions, args.reviews_export_path, edition_languages)
    log('Done')


def file_path(path):
    '''
    Helper function to validate user input.
    Path should have .csv as extension.
    Non-existing folder in path will be created.
    '''
    if not path.endswith('.csv'):
        raise argparse.ArgumentTypeError(
            'File \'{}\' should have .csv extension'.format(path))
    dir_name = os.path.dirname(path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return path


def editions_url(url):
    '''
    Helper function to validate user input.
    Url must contain 
    '''
    required_bit = '/work/editions/'
    if not required_bit in url:
        raise argparse.ArgumentTypeError(
            'editions_url should contain {}'.format(required_bit)
        )
    return url


def parse_arguments(sys_args):
    '''
    Parse the supplied arguments.
    '''
    parser = argparse.ArgumentParser(
        description='Scrape reviews for a title based on its various editions')

    parser.add_argument(
        '--editions_url', '--url', '-eu', dest='editions_url', type=editions_url, required=True,
        help="""Required. The url of an editions page. May or may not include the page queryparam at the end.
               You can find the url by clicking 'All Editions' (under 'Other Editions') on a title's page.
               Example: 'https://www.goodreads.com/work/editions/6463092-het-diner'""")

    parser.add_argument(
        '--reviews_export_path', '-rep', dest='reviews_export_path', type=file_path, required=True,
        help='''Path to the file you want to export the reviews data to. Should be a .csv file''')

    parser.add_argument(
        '--editions_export_path', '-eep', dest='editions_export_path', type=file_path,
        required=False, help='''Optional. Path to the file you want to export the editions data to.
                Should be a .csv file. Editions will not be exported if you leave this empty''')

    parser.add_argument(
        '--edition_languages', '-el', dest='edition_languages',
        choices=(EDITION_LANGUAGES.append('all')), default='all', nargs="+",
        help="Optional. Choose one or multiple from the choices. Example: '-el English German'. Defaults to 'all\'")

    parsedArgs = parser.parse_args()
    return parsedArgs


if __name__ == "__main__":
    main(sys.argv)
