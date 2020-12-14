import csv
import re
from math import log

reviews_path = './data/goodreads_tokenised.csv'
language = 'dutch'
target_pattern = r'^vertaa?l'
out_path = './data/collocations_{}.txt'.format(language)

# import reviews

with open(reviews_path) as csvfile:
    reader = csv.DictReader(csvfile)
    reviews_text = (row["tokenised_text"] for row in reader if row["language"] == language)
    reviews = [review.split() for review in reviews_text]

# frequencies

vocab = set(word for review in reviews for word in review)

def count_words():
    counts_general = {word: 0 for word in vocab}
    counts_translat =  {word: 0 for word in vocab}
    window = 4

    for review in reviews:
        for i, word in enumerate(review):
            counts_general[word] += 1

            if re.search(target_pattern, word):
                preceding = [review[j] for j in range(i - window, i) if j >= 0]
                following = [review[j] for j in range(i + 1, i + 1 + window) if j < len(review)]

                for neighbour in preceding + following:
                    counts_translat[neighbour] += 1

    return counts_translat, counts_general

def filter_counts(target, general):
    filtered_vocab = set(word for word, count in general.items() if count > 1)
    filtered_target = {word: count for word, count in target.items() if word in filtered_vocab}
    filtered_general = {word: count for word, count in general.items() if word in filtered_vocab}

    return filtered_target, filtered_general

def relative_counts(counts):
    total = sum(counts.values())
    return {word: count / total for word, count in counts.items()}

def counts_log(counts):
    return {word: log(count + 1) for word, count in counts.items()}

def relative_frequencies(target, general):
    target_log = counts_log(relative_counts(target))
    general_log = counts_log(relative_counts(general))

    return {word: target_log[word] - general_log[word] for word in target}

counts_translat, counts_general = filter_counts(*count_words())
rel_freq = relative_frequencies(counts_translat, counts_general)

def sort_by_frequency(counts):
    return sorted(counts, key = lambda w : counts[w], reverse = True)

ranking = sort_by_frequency(rel_freq)

print(ranking[:50])

#export
with open(out_path, 'w') as outfile:
    for i in range(100):
        outfile.write(ranking[i])
        outfile.write('\n')
