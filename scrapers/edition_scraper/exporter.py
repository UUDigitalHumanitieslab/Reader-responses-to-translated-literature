import csv
from utilities.utils import log, CSV_DELIMITER

def to_csv(path, editions):
    '''
    Append the editions to the csv in path.
    '''
    edition_count = len(editions)
    if edition_count < 1: return
    log("Exporting {} editions to '{}'".format(edition_count, path))
    with open(path, 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter=CSV_DELIMITER)
        writer.writerow(editions[0].get_csv_header())
        for edition in editions:
            writer.writerow(edition.to_csv_row())
