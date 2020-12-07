import spacy

class Tokeniser:
    def __init__(self, language):
        models = {
            "english" : "en_core_web_sm"
        }
        self.nlp = spacy.load(models[language])

    def process(self, review: str, lemmatise = True, filter_stopwords = True):
        doc = self.nlp(review)

        # filter punctuation and digits
        is_alpha = lambda token : token.is_alpha
        filtered_tokens =  [token for token in doc if token.is_alpha]

        # filter named entities
        # make an exception for language and nationality names
        accepted_ent_types = ['', 'LANGUAGE', 'NORP']
        is_not_NE = lambda token: token.ent_type_ in accepted_ent_types

        # filter stopwords
        is_not_stopword = lambda token: token.is_stop == False

        # apply all filters
        filters = [is_alpha, is_not_NE]
        if filter_stopwords:
            filters.append(is_not_stopword)
        filtered_tokens = [token for token in doc if all(f(token) for f in filters)]

        # convert tokens to lemmas or text
        if lemmatise:
            words = [token.lemma_.lower() for token in filtered_tokens]
        else:
            words = [token.text.lower() for token in filtered_tokens]

        return words
