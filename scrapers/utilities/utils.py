CSV_DELIMITER = ";"

def log(message):
    '''
    Log a message.
    For now simply calls `print()`
    '''
    print(message)


def remove_whitespace(text):
    '''
    Remove all whitespaces and join words with a space
    '''
    return " ".join(text.split())


def get_number_of_pages(total_items, items_per_page):
    '''
    Given a certain number of items per page,
    establish the number of pages we need to collect.

    Neat trick to get rounded integers from https://stackoverflow.com/a/23590097.
    '''
    return int(total_items / items_per_page) + (total_items % items_per_page > 0)
