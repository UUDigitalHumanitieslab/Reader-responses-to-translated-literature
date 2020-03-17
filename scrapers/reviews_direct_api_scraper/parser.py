from bs4 import BeautifulSoup
from review_utils.review import Review

def parse_html(html, edition):
    '''
    Parse a single response from the GoodReads review api (i.e. 'https://www.goodreads.com/book/reviews/').
    This reponse should be the HTML of a (sub)page of reviews, typically max. 30.
    Returns an array of Reviews.
    '''
    soup = BeautifulSoup(html, 'html.parser')
    reviews = soup.find_all("div", class_="review")
    results = []
    for r_html in reviews:
        review = Review()
        review.id = r_html['id']
        review.language = edition.language
        review.edition_id = edition.get_edition_id()
        review.author = get_text_or_none(r_html.find("a", class_="user"))
        review.date = get_text_or_none(r_html.find("a", class_="reviewDate"))
        review.text = get_text(r_html)
        review.rating = get_text_or_none(r_html.find("span", class_="staticStar"))
        results.append(review)
    return results

def get_text(review_html):
    text = None
    if review_html:
        review_text_elem = review_html.find("div", class_="reviewText")    
        if review_text_elem:
            text = get_text_or_none(review_text_elem.find("span", class_="readable"))
    return text

def get_text_or_none(field):
    if field: return field.get_text()
    return None
