import csv
import re
import pandas as pd
from typing import List, Dict
from collections import defaultdict
from collocations.patterns import LANGUAGES_PATTERNS

WORDS_PATH = './data/word_classes.csv'
INPUT_FACTORS = ['original_language', 'edition_language', 'language', 'age_category', 'book_genre', 'rating_no']
WINDOW_SIZE = 4

def read_categories(words_path):
    with open(WORDS_PATH) as words_file:
        reader = csv.DictReader(words_file)
        word_categories = {language : defaultdict(lambda : 'other') for language in LANGUAGES_PATTERNS}

        for row in reader:
            language = row['language']
            word = row['word']
            cat = row['category']
            word_categories[language][word] = cat

    categories_generator = (value for lang_data in word_categories.values() for value in lang_data.values())
    categories = list(sorted(set(categories_generator)))

    return word_categories, categories


def output_count(words: List[str], word_categories: Dict, categories: List):
    counts = {cat : 0 for cat in categories}

    for word in words:
        cat = word_categories[word]
        counts[cat] += 1

    return counts   

def count_data(reviews_path, language = 'english'):
    '''Create a table with one row for each mention of "translation". Includes
    some info about the review and the categories of words in the context window.'''
    # import word categories
    word_categories, categories = read_categories(WORDS_PATH)

    # import reviews
    with open(reviews_path) as reviews_file:
        reader = csv.DictReader(reviews_file)

        all_data = []

        for row in reader:
            text = row['tokenised_text']
            language = row['language'].lower()
            if language in LANGUAGES_PATTERNS:
                pattern = LANGUAGES_PATTERNS[language]
                words = text.split()
                input_data = { factor : row[factor] for factor in INPUT_FACTORS}

                for i, word in enumerate(words):
                    if re.search(pattern, word):
                        preceding = [words[j] for j in range(i - WINDOW_SIZE, i) if j >= 0]
                        following = [words[j] for j in range(i + 1, i + 1 + WINDOW_SIZE) if j < len(words)]
                        window = preceding + following
                        output_data = output_count(window, word_categories[language], categories)

                        data = {**input_data, **output_data}
                        all_data.append(data)

    df = pd.DataFrame(all_data, columns=INPUT_FACTORS + categories)
    return df

def mentions_translation(text, language):
    if language in LANGUAGES_PATTERNS:
        pattern = LANGUAGES_PATTERNS[language]
        words = text.split()
        return any(re.search(pattern, word) for word in words)
    else:
        return None

def count_data_per_review(reviews_path):
    '''Create table with one row for each review. Similar to the 
    readit output, but  but with some extra info. We also ignore some
    columns like the full text.'''

    with open(reviews_path) as reviews_file:
        reader = csv.DictReader(reviews_file)

        def review_data(row):
            input_data = { factor : row[factor] for factor in INPUT_FACTORS}
            is_translated = row['original_language'] != row['edition_language']
            mentions = mentions_translation(row['tokenised_text'], row['language'].lower())
            data = {
                **input_data,
                'is_translated': is_translated,
                'mentions_translation': mentions,
            }
            return data
        
        all_data = [review_data(row) for row in reader]


    df = pd.DataFrame(all_data, columns = INPUT_FACTORS + ['is_translated', 'mentions_translation'])
    return df