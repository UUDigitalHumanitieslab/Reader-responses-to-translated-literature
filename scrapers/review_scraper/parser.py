from bs4 import BeautifulSoup
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from utilities.review import Review
from utilities.utils import remove_whitespace

class ReviewPageParser:

    def __init__(self, html, edition):
        self.edition = edition
        self.soup = BeautifulSoup(html, 'html.parser')
        self.reviews = self.soup.find_all('div', class_='review')
    
    def contains_only_reviews(self):
        '''
        Establish if this is a page with only reviews or not.
        If it isn't, there are ratings in the review list.
        '''
        review_texts = self.get_reviews_texts()
        return len(review_texts) == len(self.reviews)

    def is_top_300(self):
        '''
        Establish if the current page is part of a Top 300.
        Ideal for checking if a text_only request returns all results,
        or if collecting per rating is necessary.
        '''
        count_elem = self.get_count_element()
        return 'top 300' in count_elem.text.lower()

    def get_number_of_text_only_reviews(self):
        '''
        Get the total number of text-only reviews for the edition (optionally limited to rating).
        This number is based on the 'Displaying X of Y' field. Therefore, if the current page
        is based on a rating, the number returned represent the total number of text-only reviews
        for the edition. Note that the current page contains only a subselection of this total.
        Returns 300 if current page is part of a top 300.
        '''
        if (self.is_top_300()):
            return 300
        count_elem = self.get_count_element()
        if not ' of ' in count_elem.text:
            return 0
        words = remove_whitespace(count_elem.text).strip().split(' ')
        return int(words[3])

    def has_alternate_ratings(self, rating):
        '''
        Check if the current page has any ratings other than `rating`. Typically, this implies
        that the current page has only ratings with the value of `rating` (no reviews with text), 
        and these are supplemented with ratings and reviews of different scores.
        '''
        result = False
        for review in self.reviews:
            stars_count = len(review.find('div', class_='reviewHeader').find_all('span', class_='staticStar p10'))
            if not stars_count == rating:
                result = True
                break
        return result


    def get_count_element(self):
        '''
        Extract the element containg the 'Displaying X of Y reviews' text.
        '''
        return self.soup.find('div', class_='reviewSearchResults__count')

    def get_reviews_texts(self):
        '''
        Get only the reviews that contain text (i.e. ignore ratings)
        '''
        return self.soup.find_all('div', class_='reviewText')

    def get_reviews(self):
        '''
        Get Review instances parsed from the page's HTML.
        Ignores ratings (i.e. reviews without text)
        '''
        reviews = []
        for review_html in self.reviews:
            review_text = review_html.find('div', class_='reviewText')
            if not review_text:
                continue
            review = Review()
            review.id = review_html['id']
            review.url = review_html.find('link')['href']
            review.edition_language = self.edition.language
            review.edition_id = self.edition.get_id()
            review.author = self.get_text_or_none(review_html.find('a', class_='user'))
            review.date = self.get_text_or_none(review_html.find('a', class_='reviewDate'))
            review.text = self.extract_review(review_text)
            review.rating = self.get_text_or_none(review_html.find('span', class_='staticStar'))
            if review.text:
                try:
                    review.language = detect(review.text)
                except LangDetectException:
                    # langdetect can't deal with texts that consist of only things like
                    # '3.5-4/5', or '(...) 6/10'
                    review.language = 'UNKNOWN'
            reviews.append(review)
        return reviews        

    def extract_review(self, review_text_elem):
        container = review_text_elem.find('span', class_='readable')
        # always extract the text from the last <span>.
        return self.get_text_or_none(container.find_all('span')[-1])

    def get_text_or_none(self, field):
        if field: return remove_whitespace(field.get_text(' '))
        return None
