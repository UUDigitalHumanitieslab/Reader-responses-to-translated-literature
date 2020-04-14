
class Review:

    def __init__(self):
        self.id = None
        self.url = None
        self.edition_id = None
        self.edition_language = None
        self.date = None
        self.author = None
        self.language = None
        self.rating = None
        self.text = None

    def get_csv_header(self):
        return list(self.to_dict().keys())

    def from_csv(self, row):
        self.id = row[0]
        self.url = row[1]
        self.edition_id = row[2]
        self.edition_language = row[3]
        self.date = row[4]
        self.author = row[5]
        self.language = row[6]
        self.rating = row[7]
        # ignore rating as number, i.e. row[8]
        self.text = row[9]

    def to_dict(self):
        '''
        Get a dict representing the review.
        Ideal for writing to csv using a DictWriter.
        '''
        return {
            'id': self.id,
            'url': self.url,
            'edition_id': self.edition_id,
            'edition_language': self.edition_language,
            'date': self.date,
            'author': self.author,
            'language': self.language,
            'rating': self.rating,
            'rating_no': self.get_rating_as_number(),
            'text': self.text
        }

    def get_rating_as_number(self):
        '''
        Translate a number between 1 and 5 to the GoodReads equivalent
        '''
        if self.rating == 'did not like it':
            return 1
        if self.rating == 'it was ok':
            return 2
        if self.rating == 'liked it':
            return 3
        if self.rating == 'really liked it':
            return 4
        if self.rating == 'it was amazing':
            return 5
