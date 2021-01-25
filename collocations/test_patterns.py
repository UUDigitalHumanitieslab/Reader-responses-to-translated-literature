# print the set of words that match the pattern for each language

import csv
import re
from collocations.patterns import LANGUAGES_PATTERNS

reviews_path = './data/goodreads_tokenised.csv'

matching_words = {language: set() for language in LANGUAGES_PATTERNS}

with open(reviews_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        language = row['language'].lower()
        words = row['tokenised_text'].split()

        is_match = lambda word: re.search(LANGUAGES_PATTERNS[language], word)
        matches = filter(is_match, words)
        for match in matches:
            matching_words[language].add(match)

for language in matching_words:
    print(language.upper())
    print()
    print(matching_words[language])
    print()