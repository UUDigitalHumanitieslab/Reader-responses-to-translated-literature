class Edition:
    def __init__(self):
        self.title = None
        self.url = None
        self.authors = []
        self.pub_details = None
        self.edition_details = None
        self.isbn = None
        self.isbn13 = None
        self.asin = None
        self.language = None
        self.avg_rating = None
        self.number_of_ratings = None

    def get_csv_header(self):
        return list(vars(self).keys())

    def from_csv_row(self, row):
        self.title = row[0]
        self.url = row[1]
        self.authors = row[2].split(',')
        self.pub_details = row[3]
        self.edition_details = row[4]
        self.isbn = row[5]
        self.isbn13 = row[6]
        self.asin = row[7]
        self.language = row[8]
        self.avg_rating = row[9]
        self.number_of_ratings = row[10]
        return self

    def to_csv_row(self):
        return [
            self.title,
            self.url,
            ",".join(self.authors),
            self.pub_details,
            self.edition_details,
            self.isbn,
            self.isbn13,
            self.asin,
            self.language,
            self.avg_rating,
            self.number_of_ratings,
        ]

    def __str__(self):
        return str(self.title)
