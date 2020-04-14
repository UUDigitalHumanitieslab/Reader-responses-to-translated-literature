from .utils import get_number_of_pages

def test_get_number_of_pages():
    assert get_number_of_pages(137, 100) == 2
    assert get_number_of_pages(6, 100) == 1
    assert get_number_of_pages(543, 100) == 6
    assert get_number_of_pages(100, 100) == 1
    assert get_number_of_pages(101, 100) == 2
    assert get_number_of_pages(261, 30) == 9
    assert get_number_of_pages(30, 30) == 1
    assert get_number_of_pages(31, 30) == 2
    assert get_number_of_pages(160, 30) == 6