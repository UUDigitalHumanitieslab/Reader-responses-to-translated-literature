import sys
from .collector import collect
from .exporter import Exporter
from utilities.utils import log

def scrape(editions, output_path, edition_languages=['English', 'Dutch', 'German', 'Spanish', 'French']):
    '''
    Parameters:
        editions -- List of Edition instances to collect reviews for
        output_path -- a full path (incl. filename and extension) where you expect the output.
        edition_languages -- specify the languages to include when collecting editions.
            Example: ['English', 'Dutch', 'German', 'Spanish', 'French']
            All other languages will be ignored. Defaults to ['English', 'Dutch', 'German', 'Spanish', 'French']
    '''
    exporter = Exporter()
    reviews = []
    used_editions = 0
    editions_length = len(editions)

    for index, edition in enumerate(editions):
        if edition.language in edition_languages:
            log("Collecting reviews for edition '{}' [{}/{}]".format(edition.get_id(), index + 1, editions_length))
            used_editions += 1
            reviews.extend(collect(edition))

    log("{} reviews collected from {} editions".format(len(reviews), used_editions))

    exporter.to_csv(output_path, reviews)
