class Edition:
    
    def from_csv_row(self, row):
        self.url = row[0]
        self.pub_details = row[1]
        self.edition_details = row[2]
        self.author = row[3]
        self.isbn =  row[4]
        self.language = row[5]
        self.rating = row[6]
        return self

    def get_edition_id(self):
        index = self.url.rfind('/')
        return self.url[index + 1:]

    def __str__(self):
        return str(self.get_edition_id())
