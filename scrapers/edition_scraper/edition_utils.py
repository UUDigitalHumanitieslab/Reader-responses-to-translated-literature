import os
import sys
import csv

from .edition import Edition


def parse_editions_csv(path):
    '''
    Parse a CSV file to Edition instances.
    Returns an array of Editions.
    '''
    editions = []
    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=",")    
        for row in reader:
            e = Edition()
            editions.append(e.from_csv_row(row))
    return editions


def get_editions(path, languages):
    '''
    Get ids (e.g. '41022071-le-diner') from the csv for editions in the specified languages
    '''
    results = []
    all_editions = parse_editions_csv(path)
    for e in all_editions:
        if e.language in languages:
            results.append(e)
    return results
