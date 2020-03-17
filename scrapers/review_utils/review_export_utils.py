import csv

class Exporter:
    csv_header_written = False

    def to_csv(self, path, fieldnames, reviews):
        '''
        Append the reviews to the csv in path.
        Write fieldnames as the first row / header.
        '''
        with open(path, 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if not self.csv_header_written: 
                writer.writeheader()
                self.csv_header_written = True
            for r in reviews:
                writer.writerow(r.to_dict())


def get_new_reviews(path, reviews):
    '''
    From 'reviews', extract the reviews that do not exist in the csv (at 'path') yet.
    '''
    try:
        with open(path, newline='') as f:
            reader = csv.reader(f)
            existing_reviews = list(reader)

        if existing_reviews:
            new_reviews = []
            for review in reviews:
                if not already_exists(existing_reviews, review):
                    new_reviews.append(review)
            return new_reviews
        else:
            return reviews
    except:
        return reviews


def already_exists(existing_reviews, review):
    for existing_review in existing_reviews:
        if review.id == existing_review[0]:
            return True
    return False
