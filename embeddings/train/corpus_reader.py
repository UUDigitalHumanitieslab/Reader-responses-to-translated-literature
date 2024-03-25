import csv
from gensim import utils
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import brown
import re

def token(word):
    if re.match('^(\d)+$', word):
        return '<NUM>'
    if not re.search('\w', word):
        return '<PUNCT>'
    return word.lower()

class ReviewCorpus():
    def __init__(self, path, split_sentences = True):
        self.split_sents = split_sentences
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)
            reviews = [row["text"] for row in reader]
        
        self.reviews = [self.preprocess(review) for review in reviews]     

    def __len__(self):
        if self.split_sents:
            return sum(len(review) for review in self.reviews)
        else:
            return len(self.reviews)

    def __iter__(self):
        for review in self.reviews:
            if self.split_sents:
                for sent in review:
                    yield sent
            else:
                yield review

    def preprocess(self, review):
        def tokens(string):
            return [token(word) for word in word_tokenize(string)]

        if self.split_sents:
            sents = sent_tokenize(review)
            return [tokens(sent) for sent in sents]
        else:
            return tokens(review)

class BrownCorpus():
    def __init__(self):
        pass

    def __iter__(self):
        for sent in brown.sents():
            words = [token(word) for word in sent]
            yield words

