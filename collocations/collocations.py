import csv
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import re
from math import log

reviews_path = '../data/reviews_about_translation.csv'
out_path = 'collocations.txt'

# import reviews

with open(reviews_path) as csvfile:
    reader = csv.DictReader(csvfile)
    reviews = [row["text"] for row in reader]

# preprocessing

stops = set(stopwords.words("english"))
stops.add("'s")
stops.add("n't")
stops.add("'m")

def process_sent(sent):
    words = [w.lower() for w in word_tokenize(sent)]

    def include(word):
        if not re.search(r'\w', word):
            return False
        if word in stops:
            return False
        return True

    filtered_words = [w for w in words if include(w)]
    return filtered_words

def process_review(review):
    sents = sent_tokenize(review)
    return [process_sent(s) for s in sents]

processed_reviews = [process_review(r) for r in reviews]

vocab = set(word for review in processed_reviews for sent in review for word in sent)

# frequencies

def count_words():
    counts_general = {word: 0 for word in vocab}
    counts_translat =  {word: 0 for word in vocab}
    translat_pat = r'^translat'
    window = 5

    for review in processed_reviews:
        for sent in review:
            for i, word in enumerate(sent):
                counts_general[word] += 1

                if re.search(translat_pat, word):
                    preceding = [sent[j] for j in range(i - window, i) if j >= 0]
                    following = [sent[j] for j in range(i + 1, i + 1 + window) if j < len(sent)]

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

#export
with open(out_path, 'w') as outfile:
    for i in range(50):
        outfile.write(ranking[i])
        outfile.write('\n')