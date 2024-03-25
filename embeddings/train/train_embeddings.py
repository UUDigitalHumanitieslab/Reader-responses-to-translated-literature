from gensim import models

def train(sentences, pretrained = None, window = 5):
    if pretrained:
        #train from new sentences
        pretrained.build_vocab(sentences, update=True)
        pretrained.train(
            sentences, 
            total_examples=len(sentences), epochs=pretrained.iter
            )
        return pretrained
    else:
        model = models.Word2Vec(
            sentences = sentences, 
            size=100, window=window
            )
        return model