from bs4 import BeautifulSoup
from .edition import Edition


class EditionPageParser():
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_number_of_editions(self):
        '''
        Extract the total number of editions from the HTML of a full editions page.
        '''
        text = self.soup.find("div", class_="showingPages").find("span").text.strip()
        index = text.rfind(' ')
        return int(text[index + 1:])

    def get_editions(self):
        editions = []
        edition_elems = self.soup.find_all("div", class_="editionData")
        for elem in edition_elems:
            editions.append(self.get_edition(elem))
        return editions

    def get_edition(self, edition_data_elem):
        '''
        Extract an instance of edition from an HTML element with class 'editionData'.
        '''
        edition = Edition()
        data_rows = edition_data_elem.find_all("div", class_="dataRow")

        for row in data_rows:
            authorName_containers = row.find_all(
                'div', class_='authorName__container')
            book_title = row.find('a', class_='bookTitle')

            if authorName_containers:
                edition.authors = self.get_authors(authorName_containers)
            elif book_title:
                edition.title, edition.url = self.get_title_and_url(book_title)
            else:
                self.process_anonymous_data_row(row, edition)

        return edition

    def process_anonymous_data_row(self, row, edition):
        '''
        Process data rows that do not have an explicit title / identifier.
        '''
        data_title = row.find('div', class_='dataTitle')
        if data_title:
            title_text = data_title.text.lower()
            data_value = row.find('div', class_='dataValue')
            if 'isbn' in title_text:
                self.set_isbns(title_text, data_value, edition)
            elif 'edition language' in title_text:
                edition.language = data_value.text.strip()
            elif 'average rating' in title_text:
                self.set_rating_details(data_value, edition)
            elif 'asin' in title_text:
                edition.asin = data_value.text.strip()
        else:
            text = row.text.strip()
            if 'published' in text.lower():
                edition.pub_details = self.remove_whitespace(text)
            elif not text == 'more details' and not text == 'less detail':
                edition.edition_details = self.remove_whitespace(text)

    def set_rating_details(self, data_value, edition):
        text = data_value.text.strip()
        # print(text)
        index = text.index(' ')
        edition.avg_rating = float(text[:index])
        index_start = text.index('(') + 1
        index_end = text.rfind(' ')
        edition.number_of_ratings = int(text[index_start:index_end].replace(',', ''))

    def set_isbns(self, title_text, data_value, edition):
        text = data_value.text.strip()
        if title_text.strip().lower() == 'isbn13:':
            edition.isbn13 = self.remove_whitespace(text)
        else:
            isbn = text
            if ' ' in text:
                index = text.index(' ')
                isbn = self.remove_whitespace(text[:index])
            edition.isbn = isbn
            if data_value.find('span'):
                edition.isbn13 = self.get_isbn_13(data_value)

    def get_isbn_13(self, data_value):
        text = self.remove_whitespace(data_value.find('span').text)
        index = text.rfind(':')
        return self.remove_whitespace(text[index + 2:len(text) - 1])

    def get_authors(self, authorName_containers):
        '''
        Extract authors (incl roles).
        '''
        authors = []
        for c in authorName_containers:
            author = c.find('a').text
            role = c.find('span', {'class': ['authorName', 'role']})
            if role:
                author = '{} {}'.format(author, role.text)
            authors.append(author)
        return authors

    def get_title_and_url(self, book_title):
        return self.remove_whitespace(book_title.text), book_title['href']

    def remove_whitespace(self, text):
        '''
        Remove all whitespaces and join words with a space
        '''
        return " ".join(text.split())
