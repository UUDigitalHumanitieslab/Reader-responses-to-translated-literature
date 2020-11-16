from gensim import models

EMBEDDINGS_PATH = "embeddings/with_pretraining"

model = models.Word2Vec.load(EMBEDDINGS_PATH)

#automatic evaluation
print('QUESTION ANSWER DATASET')
accuracy = model.accuracy("eval/questions-words.txt")

for section in accuracy:
    name = section['section']
    correct = len(section['correct'])
    incorrect = len(section['incorrect'])
    print('{}: {} out of {}'.format(name, correct, incorrect))


#manual inspection
print()
words = ['book', 'author', 'genre', 'boring', 'recommend', 'translation']

print('WORD SIMILARITES')
for word in words:
    neighbours = [neighbour for neighbour, score in model.most_similar(word)]
    print("'{}' is most similar to '{}', '{}', or '{}'".format(word, neighbours[0], neighbours[1], neighbours[2]))
