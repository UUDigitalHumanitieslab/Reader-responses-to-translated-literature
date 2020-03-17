
class Review:

    def __init__(self):
        self.id = ""
        self.edition_id = ""
        self.date = ""
        self.language = ""
        self.author = ""
        self.rating = ""
        self.text = ""

    def from_csv(self, row):
        self.id = row[0]
        self.edition_id = row[1]
        self.date = row[2]
        self.language = row[3]
        self.author = row[4]
        self.rating = row[5]
        self.text = row[6]

    
    def to_dict(self):
        '''
        Get a dict representing the review.
        Ideal for writing to csv using a DictWriter.
        Note that all newlines ('\\r' and '\\n') will be removed from the text field.
        '''
        return {
            'review_id': self.id,
            'edition_id': self.edition_id,
            'review_date': self.date,
            'review_language': self.language,
            'author': self.author, 
            'rating': self.rating, 
            'text': self.parse_text(self.text)
        }


    def parse_text(self, text):
        '''
        Remove all arriage returns and newlines from the review text
        '''
        return text.replace("\n", "").replace("\r", "")
