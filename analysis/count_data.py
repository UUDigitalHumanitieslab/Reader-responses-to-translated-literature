import csv
import re
import pandas as pd
from typing import List, Dict
from collections import defaultdict
from collocations.patterns import LANGUAGES_PATTERNS

WORDS_PATH = './data/word_classes.csv'

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
    # import word categories
    word_categories, categories = read_categories(WORDS_PATH)

    # import reviews

    input_factors = ['original_language', 'edition_language', 'language', 'age_category', 'book_genre', 'rating_no']

    with open(reviews_path) as reviews_file:
        reader = csv.DictReader(reviews_file)
        window_size = 4

        all_data = []

        for row in reader:
            text = row['tokenised_text']
            language = row['language'].lower()
            if language in LANGUAGES_PATTERNS:
                pattern = LANGUAGES_PATTERNS[language]
                words = text.split()
                input_data = { factor : row[factor] for factor in input_factors}

                for i, word in enumerate(words):
                    if re.search(pattern, word):
                        preceding = [words[j] for j in range(i - window_size, i) if j >= 0]
                        following = [words[j] for j in range(i + 1, i + 1 + window_size) if j < len(words)]
                        window = preceding + following
                        output_data = output_count(window, word_categories[language], categories)

                        data = {**input_data, **output_data}
                        all_data.append(data)

    df = pd.DataFrame(all_data, columns=input_factors + categories)
    return df