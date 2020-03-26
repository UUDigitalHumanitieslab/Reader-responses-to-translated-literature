'''
Configuration.
'''
TITLE ='The_philosophers_stone'

# 'https://www.goodreads.com/work/editions/4640799-harry-potter-and-the-philosopher-s-stone'
# 'https://www.goodreads.com/work/editions/6463092-het-diner'

# for editions list scape, the editions URL of Goodreads
ALL_EDITIONS_URL = 'https://www.goodreads.com/work/editions/4640799-harry-potter-and-the-philosopher-s-stone'

# editions csv title that will be created to store the list of all editions, to be scraped from this list
EDITIONS_CSV = 'Harry_Potter_phil_stone_editions_goodreads.csv' 

#specify the languages of the editions that must be scraped, in the format of goodreads in the created editions_csv
EDITION_LANGUAGES=['English', 'Dutch', 'Spanish', 'French', 'German'] 