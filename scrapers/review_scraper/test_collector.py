from .collector import get_number_of_pages, get_page_url, base_url
from utilities.edition import Edition

def test_get_page_url():
    e = Edition()
    e.url = 'whatever/id'
    url = get_page_url(base_url, e, 1)
    assert url == 'https://www.goodreads.com/book/reviews/id?edition_reviews=true&text_only=true&page=1'

    url = get_page_url(base_url, e, 5, 5)
    assert url == 'https://www.goodreads.com/book/reviews/id?edition_reviews=true&rating=5&page=5'

