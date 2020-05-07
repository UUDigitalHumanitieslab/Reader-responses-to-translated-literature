import os
from .parser import ReviewPageParser
from utilities.edition import Edition

fake_edition = Edition()

test_pages = [
    {
        'file': '9673614-la-cena_1.html',
        'review_count': 30,  # this count excludes ratings (if applicable at all)
        'only_reviews': True,
        'top_300': False,
        'edition_text_only_review_count': 104
    },
    {
        'file': '9673614-la-cena_4.html',
        'review_count': 14,
        'only_reviews': True,
        'top_300': False,
        'edition_text_only_review_count': 104
    },
    {
        'file': '15797938-the-dinner_1_10.html',
        'review_count': 30,
        'only_reviews': True,
        'top_300': True,
        'rating': 1,
        'alternate_ratings': False,
        'edition_text_only_review_count': 300
    },
    {
        'file': '15797938-the-dinner_3_6.html',
        'review_count': 30,
        'only_reviews': True,
        'top_300': True,
        'rating': 3,
        'alternate_ratings': False,
        'edition_text_only_review_count': 300
    },
    {
        'file': '15797938-the-dinner_5_1.html',
        'review_count': 30,
        'only_reviews': True,
        'top_300': True,
        'rating': 5,
        'alternate_ratings': False,
        'edition_text_only_review_count': 300
    },    
    {
        'file': '22561799-het-diner_1.html',
        'review_count': 2,
        'only_reviews': False,
        'top_300': False,
        'edition_text_only_review_count': 2
    },
    {
        'file': '28550610-harry-potter-and-the-sorcerer-s-stone_2_1.html',
        'review_count': 10, # Note that these 10 reviews are not of rating 2
        'only_reviews': False,
        'top_300': False,
        'rating': 2,
        'alternate_ratings': True,
        'edition_text_only_review_count': 0
    },
    {
        'file': '28550610-harry-potter-and-the-sorcerer-s-stone_5_4.html',
        'review_count': 30,
        'only_reviews': True,
        'top_300': True,
        'rating': 5,
        'alternate_ratings': False,
        'edition_text_only_review_count': 300 
    },
    {
        'file': '28550610-harry-potter-and-the-sorcerer-s-stone_5_10.html',
        'review_count': 2,
        'only_reviews': False,
        'top_300': True,
        'rating': 5,
        'alternate_ratings': False,
        'edition_text_only_review_count': 300 
    },
    {
        'file': '7947003-the-lost-symbol_8.html',
        'review_count': 30,
        'only_reviews': True,
        'top_300': False,
        'edition_text_only_review_count': 277
    },
]


def test_get_reviews_by_count():
    '''
    Test 'get_reviews' by simpling counting the reviews extracted.
    Quickly tests if all reviews all found in all pages.
    '''
    for page in test_pages:
        p = ReviewPageParser(get_test_page(page['file']), fake_edition)
        assert len(p.get_reviews()) == page['review_count']
        

def test_get_reviews_parsing_short():
    '''
    Test 'get_reviews' parsing capacities with a short review
    '''
    html = get_test_partial('review_short.html')
    fake_edition.url = '/parsed/for/edition_id'
    fake_edition.language = 'Klingon'
    p = ReviewPageParser(html, fake_edition)
    reviews = p.get_reviews()
    assert len(reviews) == 1
    r = reviews[0]
    assert r.edition_id == 'edition_id'
    assert r.edition_language == 'Klingon'
    assert r.id == 'review_975219334'
    assert r.url == 'https://www.goodreads.com/review/show/975219334'
    assert r.date == 'Jun 23, 2014'
    assert r.author == 'Jolieg G'
    assert r.rating == 'it was amazing'
    assert r.text == 'Met veel plezier gelezen. Vlot en boeiend geschreven en af en toe een humoristische noot. Ga vast en zeker meer van hem lezen.'

def test_get_reviews_parsing_long():
    '''
    Test 'get_reviews' parsing capacities with a long review.
    This is interesting because long review texts are in the 'reviewText' element twice:
    first a snippet and then the whole text.
    '''
    expected_text = '2/22/20. I don’t think my progress update saved on my most recent reading of this book, so since I’ve never written a review of it, now is as good a time as any. I’ve read this book so many times, and it never gets old. Read the original quite a few times, have listened to the audiobook (FANTASTIC), and now read the new illustrated version to my 6 year old while introducing him to the books for the first time. This version is beautiful, (albeit heavy) and I’m so glad we purchased it. Sharing these books with my kiddo and introducing Harry Potter for the first time is a moment I’ve waited for since he was born, and it didn’t disappoint. So much commentary from him throughout. Gasps, eyes hidden in suspense, “WHAT?!?!”, “Noo!!!”, “GRYFFINDOR!!!”, and many chuckles. We finished it last night, and he’s officially hooked. Even if I don’t always feel like I’m doing a great job as a parent, well...at least I’m raising him to love Harry Potter.'
    
    html = get_test_partial('review_long.html')
    fake_edition.url = '/parsed/for/edition_id'
    fake_edition.language = 'Klingon'
    p = ReviewPageParser(html, fake_edition)
    reviews = p.get_reviews()
    assert len(reviews) == 1
    r = reviews[0]
    assert r.edition_id == 'edition_id'
    assert r.edition_language == 'Klingon'
    assert r.id == 'review_111297896'
    assert r.url == 'https://www.goodreads.com/review/show/111297896'
    assert r.date == 'Jul 12, 2010'
    assert r.author == 'Erin'
    assert r.rating == 'it was amazing'
    assert r.text == expected_text


def test_get_reviews_field_content():
    '''
    Test available test reviews for presence of values for all fields, except rating (which can be None).
    '''
    for page in test_pages:
        p = ReviewPageParser(get_test_page(page['file']), fake_edition)
        fake_edition.url = '/parsed/for/edition_id'
        fake_edition.language = 'Klingon'
        for r in p.get_reviews():
            assert r.id is not None
            assert r.url is not None
            assert r.date is not None
            assert r.author is not None
            assert r.language is not None
            # rating, surprisingly, can be None
            # text, even more surprisingly, can be None in rare cases, see #15


def test_contains_only_reviews():
    for page in test_pages:
        p = ReviewPageParser(get_test_page(page['file']), fake_edition)
        assert p.contains_only_reviews() == page['only_reviews']


def test_is_top_300():
    for page in test_pages:
        p = ReviewPageParser(get_test_page(page['file']), fake_edition)        
        assert p.is_top_300() == page['top_300']


def test_get_number_of_text_only_reviews():
    for page in test_pages:
        p = ReviewPageParser(get_test_page(page['file']), fake_edition)
        assert p.get_number_of_text_only_reviews() == page['edition_text_only_review_count']


def get_test_partial(file):
    test_file = os.path.join(get_test_data_path('partials'), file)
    with open(test_file, 'r') as f:
        return f.read()

def get_test_page(file):
    test_file = get_test_data_path(file)
    with open(test_file, 'r') as file:
        return file.read()


def get_test_data_path(file):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testdata', file)