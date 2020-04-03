from .collector import get_page_url, get_base_url, get_number_of_pages

def test_get_page_url():
    url = 'https://www.goodreads.com/work/editions/6463092-het-diner'
    expected = 'https://www.goodreads.com/work/editions/6463092-het-diner?per_page=100&page=23'
    assert get_page_url(url, 23) == expected
    
def test_get_base_url():
    url_no_qp = "https://www.goodreads.com/work/editions/6463092-het-diner"
    url_one_qp = "https://www.goodreads.com/work/editions/6463092-het-diner?expanded=false"
    url_multiple_qp = "https://www.goodreads.com/work/editions/6463092-het-diner?expanded=false&per-page=100&page=8"
    expected = "https://www.goodreads.com/work/editions/6463092-het-diner"
    assert get_base_url(url_no_qp) == expected
    assert get_base_url(url_one_qp) == expected
    assert get_base_url(url_multiple_qp) == expected

def test_get_number_of_pages():
    assert get_number_of_pages(137) == 2
    assert get_number_of_pages(6) == 1
    assert get_number_of_pages(543) == 6
    assert get_number_of_pages(100) == 1
    assert get_number_of_pages(101) == 2
