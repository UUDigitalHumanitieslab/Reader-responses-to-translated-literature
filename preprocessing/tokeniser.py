import spacy

class Tokeniser:
    def models():
        models = {
            "english" : "en_core_web_sm",
            "dutch" : "nl_core_news_sm",
            "french" : "fr_core_news_sm",
            "german" : "de_core_news_sm",
            "italian" : "it_core_news_sm",
            "portuguese" : "pt_core_news_sm",
            "spanish" : "es_core_news_sm"
        }
        return models

    def available_languages():
        return set(Tokeniser.models().keys())

    def __init__(self, language):
        models = Tokeniser.models()
        self.nlp = spacy.load(models[language])

    def process(self, review: str, lemmatise = True, filter_stopwords = True, filter_ne = True):
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
        filters = [is_alpha]
        if filter_ne:
            filters.append(is_not_NE)
        if filter_stopwords:
            filters.append(is_not_stopword)
        filtered_tokens = [token for token in doc if all(f(token) for f in filters)]

        # convert tokens to lemmas or text
        if lemmatise:
            words = [token.lemma_.lower() for token in filtered_tokens]
        else:
            words = [token.text.lower() for token in filtered_tokens]

        return words
