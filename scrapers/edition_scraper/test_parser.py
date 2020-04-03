import os
from bs4 import BeautifulSoup
from .parser import EditionPageParser


def test_get_number_of_pages():
    parser = EditionPageParser(get_test_html(
        'full_editions_page_dinner1.html'))
    assert parser.get_number_of_editions() == 137
    parser = EditionPageParser(get_test_html(
        'full_editions_page_potter5.html'))
    assert parser.get_number_of_editions() == 757


def test_get_editions_dinner():
    parser = EditionPageParser(get_test_html(
        'full_editions_page_dinner1.html'))
    editions = parser.get_editions()
    verify_editions(editions)


def test_get_editions_potter_page1():
    parser = EditionPageParser(get_test_html(
        'full_editions_page_potter1.html'))
    editions = parser.get_editions()
    verify_editions(editions)


def test_get_editions_potter_page5():
    parser = EditionPageParser(get_test_html(
        'full_editions_page_potter5.html'))
    editions = parser.get_editions()
    verify_editions(editions)


def test_get_editions_potter_page8():
    parser = EditionPageParser(get_test_html(
        'full_editions_page_potter8.html'))
    editions = parser.get_editions()
    verify_editions(editions, 57)


def verify_editions(editions, expected_editions_count=100):
    assert len(editions) == expected_editions_count
    for edition in editions:
        assert edition.title is not None
        assert edition.url is not None
        assert len(edition.authors) > 0
        assert edition.avg_rating is not None
        assert edition.number_of_ratings is not None
        assert edition.edition_details is not None
        # language, pub_details can be empty
        # all of isbn, isbn13 and asin can be empty (i.e. no serial number available)


def test_get_edition():
    html = get_test_html('edition_data.html')
    parser = EditionPageParser(html)
    # For testing purposes, create a soup here (parser does it automatically in ctor in typical scenarios)
    soup = BeautifulSoup(html, 'html.parser')
    edition = parser.get_edition(soup)
    assert edition.title == 'The Dinner (Audio CD)'
    assert edition.url == '/book/show/16073029-the-dinner'
    assert edition.pub_details == 'Published February 12th 2013 by AudioGO'
    assert edition.edition_details == 'Audio CD, 8 pages'
    assert edition.authors == ['Herman Koch', 'Clive Mantle (Narrator)']
    assert edition.isbn == '1620645912'
    assert edition.isbn13 == '9781620645918'
    assert edition.language == 'English'
    assert edition.avg_rating == 3.47
    assert edition.number_of_ratings == 114


def get_test_html(file):
    test_file = get_test_data_path(file)
    with open(test_file, 'r') as file:
        return file.read()


def get_test_data_path(file):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testdata', file)
