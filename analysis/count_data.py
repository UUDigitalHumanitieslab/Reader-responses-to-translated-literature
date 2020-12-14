import csv
import re
import pandas as pd
from typing import List
from collections import defaultdict

WORDS_PATH = './data/word_classes.csv'

def count_data(reviews_path, language = 'english'):
    # import word categories
    with open(WORDS_PATH) as words_file:
        reader = csv.DictReader(words_file)
        word_categories = defaultdict(lambda : 'other')

        for row in reader:
            if row['language'] == language:
                word = row['word']
                cat = row['category']
                word_categories[word] = cat

    categories = list(sorted(set(word_categories.values())))

    def output_count(words: List[str]):
        counts = {cat : 0 for cat in categories}

        for word in words:
            cat = word_categories[word]
            counts[cat] += 1

        return counts

    # import reviews

    input_factors = ['original_language', 'edition_language']

    with open(reviews_path) as reviews_file:
        reader = csv.DictReader(reviews_file)
        translat_pattern = r'^translat'
        window_size = 4

        all_data = []

        for row in reader:
            text = row['tokenised_text']
            words = text.split()
            input_data = { factor : row[factor] for factor in input_factors}

            for i, word in enumerate(words):
                if re.search(translat_pattern, word):
                    preceding = [words[j] for j in range(i - window_size, i) if j >= 0]
                    following = [words[j] for j in range(i + 1, i + 1 + window_size) if j < len(words)]
                    window = preceding + following
                    output_data = output_count(window)

                    data = {**input_data, **output_data}
                    all_data.append(data)

    df = pd.DataFrame(all_data, columns=input_factors + categories)
    return df