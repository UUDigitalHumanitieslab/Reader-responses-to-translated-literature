import csv
from utilities.utils import log, CSV_DELIMITER

def to_csv(path, editions):
    '''
    Append the editions to the csv in path.
    '''
    edition_count = len(editions)
    if edition_count < 1: return
    log("Exporting {} editions to '{}'".format(edition_count, path))
    with open(path, 'a', encoding='utf-8', newline='\n') as csv_file:
        writer = csv.writer(csv_file, delimiter=CSV_DELIMITER)
        writer.writerow(editions[0].get_csv_header())
        for edition in editions:
            try:
                writer.writerow(edition.to_csv_row())
            except:
                log("Error encountered exporting edition '{}'. Printing it below for reference.".format(edition.url))
                log(edition.to_csv_row())
                # self.exported_ids.pop()
            
            
