import os
import sys
import argparse
from scrapers.edition_scraper import scraper as editions_scraper


def main(sys_args):
    args = parse_arguments(sys_args)    
    editions = editions_scraper.scrape(args.editions_url, args.editions_export_path)
    print(len(editions))


def file_path(path):
    if not path.endswith('.csv'):
        raise argparse.ArgumentTypeError('File \'{}\' should have .csv extension'.format(path))    
    dir_name = os.path.dirname(path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return path

def parse_arguments(sys_args):
    '''
    Parse the supplied arguments.
    '''
    parser = argparse.ArgumentParser(
        description='Scrape reviews for a title based on its various editions')

    parser.add_argument(
        '--editions_url', '--url', '-eu', dest='editions_url',
        required=True, help="""Required. The url of an editions page. May or may not include the page queryparam at the end.
               You can find the url by clicking 'All Editions' (under 'Other Editions') on a title's page.
               Example: 'https://www.goodreads.com/work/editions/6463092-het-diner'""")

    parser.add_argument(
        '--editions_export_path', '-eep', dest='editions_export_path', type=file_path,
        required=False, help='''Optional. Path to the file you want to export the editions data to.
                Editions will not be exported if you leave this empty''')

    parser.add_argument(
        '--edition_languages', '-el', dest='editions_languages',
        choices=('English', 'German', 'Dutch', 'French', 'Spanish', 'all'), default='all',
        help='''Optional. Choose between 'English', 'German', 'Dutch', 'French', 'Spanish' or 'all'. 
                Defaults to 'all'.''')

    parsedArgs = parser.parse_args()
    return parsedArgs


if __name__ == "__main__":
    main(sys.argv)
