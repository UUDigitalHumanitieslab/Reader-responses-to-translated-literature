import os
from train.corpus_reader import ReviewCorpus, BrownCorpus
from train.train_embeddings import train
from gensim import models

CORPUS_PATH = "../data/reviews_english.csv"    #corpus location
DST_DIR = "embeddings"                      #directory for embeddings
FILENAME = "with_pretraining"               #name of embeddings file

PRETRAIN = True     #pretrain on Brown corpus
SPLIT_SENTS = True  #split reviews into sentences
WINDOW = 5          #window size for words

#initialise corpus
print("Initialising corpus...")
sentences = ReviewCorpus(CORPUS_PATH, split_sentences=SPLIT_SENTS)

#train embeddings
if PRETRAIN:
    pretrained_name = 'pretrained'
    if WINDOW != 5:
        pretrained_name += '_w{}'.format(WINDOW)

    if not pretrained_name in os.listdir(DST_DIR):
        print('No pretrained embeddings found. Pretraining...')
        pretrain_sentences = BrownCorpus()
        pretrained = train(pretrain_sentences, window=WINDOW)
        pretrained.save(os.path.join(DST_DIR, pretrained_name))
    else:
        print('Found pretrained embeddings.')
        pretrained = models.Word2Vec.load(os.path.join(DST_DIR, pretrained_name))

    print('Training model...')
    model = train(sentences, pretrained = pretrained)
else:
    print('Training model...')
    model = train(sentences, window=WINDOW)

#export
out_path = os.path.join(DST_DIR, FILENAME)

print("Saving model to '{}'...".format(out_path))
model.save(out_path)