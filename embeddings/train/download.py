#download brown corpus

import nltk

nltk.download('brown')

#download question answer dataset

import requests

url = 'https://raw.githubusercontent.com/RaRe-Technologies/gensim/develop/docs/notebooks/datasets/questions-words.txt'
r = requests.get(url)
with open('eval/questions-words.txt', 'wb') as file:
    file.write(r.content)