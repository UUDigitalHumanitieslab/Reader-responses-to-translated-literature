from .edition import Edition


def test_get_csv_header():
    e = Edition()
    assert e.get_csv_header() == [
        'title',
        'url',
        'authors',
        'pub_details',
        'edition_details',
        'isbn',
        'isbn13',
        'asin',
        'language',
        'avg_rating',
        'number_of_ratings'
    ]


def test_to_csv_row():
    edition = Edition()
    edition.title = 'The Dinner (Audio CD)'
    edition.url = 'https://goodreads.com/book/show/16073029-the-dinner'
    edition.pub_details = 'Published February 12th 2013 by AudioGO'
    edition.edition_details = 'Audio CD, 8 pages'
    edition.authors = ['Herman Koch', 'Clive Mantle (Narrator)']
    edition.isbn = '1620645912'
    edition.isbn13 = '9781620645918'
    edition.language = 'English'
    edition.avg_rating = 3.47
    edition.number_of_ratings = 114
    row = edition.to_csv_row()
    assert len(row) == 11
    assert row == [
        'The Dinner (Audio CD)',
        'https://goodreads.com/book/show/16073029-the-dinner',
        'Herman Koch,Clive Mantle (Narrator)',
        'Published February 12th 2013 by AudioGO',
        'Audio CD, 8 pages',
        '1620645912',
        '9781620645918',
        None,
        'English',
        3.47,
        114
    ]

def test_get_id():
    edition = Edition()
    assert edition.get_id() == None
    edition.url = 'https://goodreads.com/book/show/16073029-the-dinner'
    assert edition.get_id() == '16073029-the-dinner'
    