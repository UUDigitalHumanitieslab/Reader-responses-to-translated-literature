from .collector import collect as collect_editions
from .exporter import to_csv
from utilities.utils import log

def scrape(url, export_file):
    '''
    Scrape the details of all editions of a title. 

    Parameters:
        url -- The url of an editions page. May or may not include the page queryparam at the end.
               You can find the url by clicking 'All Editions' (under 'Other Editions') on a title's page.
        export_file -- Optional. The file to export the editions to, must be a .csv file. If not provided, no export is created.
    '''
    if export_file and not export_file.lower().endswith('.csv'):
        raise ValueError('export file must be a \'.csv\' file')

    editions = collect_editions(url)
    log("{} editions collected from '{}'".format(len(editions), url))

    if export_file:
        to_csv(export_file, editions)

    return editions
