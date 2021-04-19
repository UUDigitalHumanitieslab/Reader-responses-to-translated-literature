import pandas as pd
from collections import Counter
import re

LANGUAGES_PATTERNS = {
    'dutch' :  r'^vertaa?l',
    'english' : r'^translat',
    'french' : r'^tradu',
    'german' : r'[uü]bersetz',
    'italian' : r'^tradu',
    'portuguese' : r'^tradu',
    'spanish' : r'^tradu',
}

LANGUAGES = ['English', 'Dutch', 'German']
SENTIMENTS_FILE = 'collocations_sentiments.csv'
WINDOW_SIZE = 4
INPUT_FACTORS = ['id', 'original_language', 'edition_language', 'book_title', 'language', 'age_category', 'book_genre', 'rating_no', 'is_translated', 'mention_count']

def create_lemma_valence_list():
    output_list = []
    for lang in LANGUAGES:
        df = pd.read_csv('{}_ratings.csv'.format(lang), dtype='category')
        ncols = len(list(df))
        for i, row in df.iterrows():
            cats = Counter(row[1:]).most_common(1)
            # if at least two annotators agree and the category is not NaN
            if cats[0][1]>=2 and isinstance(cats[0][0], str):
                output_list.append({'word': row['word'], 'language': lang, 'category': cats[0][0]})
    output_df = pd.DataFrame(output_list)
    output_df.to_csv(SENTIMENTS_FILE, index=False)

def count_sentiments(reviews_file):
    reviews = pd.read_csv(reviews_file)
    sentiments = pd.read_csv(SENTIMENTS_FILE)
    write_header = True
    for i, row in reviews.iterrows():
        if row['mentions_translation'] and row['language'] in LANGUAGES:
            words = row['tokenised_text'].split(" ")
            pattern = LANGUAGES_PATTERNS[row['language'].lower()]
            data = { factor : row[factor] for factor in INPUT_FACTORS}
            data.update({'P': 0, 'H': 0, 'N': 0})
            relevant_sentiments = sentiments[sentiments['language']==row['language']]
            for k, word in enumerate(words):
                if re.search(pattern, word):
                    relevant_words = [words[j] for j in range(k - WINDOW_SIZE, k + WINDOW_SIZE + 1) if 0 <= j < len(words)]
                    for m, sen in relevant_sentiments.iterrows():
                        if sen['word'] in relevant_words:
                            data[sen['category']] += 1
            output = pd.DataFrame(data, index=[i])
            output.to_csv('reviews_PHN.csv', mode='a', header=write_header)
            write_header = False
