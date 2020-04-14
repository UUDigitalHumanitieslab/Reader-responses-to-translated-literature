import csv
from utilities.utils import log, CSV_DELIMITER


class Exporter:
    csv_header_written = False

    def __init__(self, unique=True):
        '''
        New instance of exporter.

        Parameters:
            unique -- export only unique reviews, i.e. no duplicates. Defaults to True.
        '''
        if unique:
            self.unique = unique
            self.exported_ids = []

    def to_csv(self, path, reviews):
        '''
        Append the reviews to the csv in path.
        Write fieldnames as the first row / header.
        '''
        if not reviews or len(reviews) == 0:
            raise ValueError("'reviews' cannot be None or an empty list")

        with open(path, 'a') as csv_file:
            writer = csv.DictWriter(
                csv_file, fieldnames=reviews[0].get_csv_header(), delimiter=CSV_DELIMITER)
            if not self.csv_header_written:
                writer.writeheader()
                self.csv_header_written = True
            for r in reviews:
                if not self.unique or (self.unique and not self.already_exported(r)):
                    writer.writerow(r.to_dict())

        log("{} {}reviews exported to '{}'".format(
            len(self.exported_ids), "(unique) " if self.unique else "", path))

    def already_exported(self, review):
        '''
        Check if a review was already exported.
        If it wasn't, store its id in 'self.exported_ids'
        '''
        if review.id in self.exported_ids:
            return True
        else:
            self.exported_ids.append(review.id)
            return False
