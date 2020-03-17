import os
from .parser import parse_html

def test_parse_html():
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'example.html')
    with open(test_file, 'r') as html_file:
        html = html_file.read()
        reviews = parse_html(html, 'test_edition', 'test_language')
        assert len(reviews) == 30

        for r in reviews:
            assert r.date is not None
            assert r.text is not None and r.text != ""
