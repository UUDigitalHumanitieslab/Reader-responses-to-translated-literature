# Reader-responses-to-translated-literature

The script will scrape reviews from Goodreads. It is a python script, that requires a python installation, (about vs 3.6). It interacts with Selenium (https://www.selenium.dev/) to do the scraping. 

### Requirements

Geckodriver for selenenium. The driver for windows lives already in this Git repo in the folder /geckodriver. If it is not there, you can download it here: https://github.com/mozilla/geckodriver/releases . Than put it in the folder /geckodriver. Replace the windows driver it if you are on Linux or a mac.



### Running

1. For scraping all editions from a particular work, find in https://www.goodreads.com the url that lists all editions. I.e. https://www.goodreads.com/work/editions/4640799-harry-potter-and-the-philosopher-s-stone, the all editions url for a Harry Potter work.

   Enter in config.py this particular url.

   Enter in config.py the title of the work. All output files that are made will have this title as prefix.

   You can also specify the edition languages that you want to scrape.

   Now you must scrape this url with the command: 'python scrape.py makelist'. The celenium browser will popup and you will see the scraping in action. If the browser does not start, you probably have a problem with the driver. It needs to be in the folder /geckodriver, and must be found by the script.

   A CSV will be made that contains the editions and particulars per edition, such as language. 

2. Start iterating the list you just made with the command 'python scrape.py edition all'

   The first edition from the list will be scraped, continuing with the next one, if all goes well. Two kinds of files are made. Per edition a csv file is created with all reviews per edition in the folder /CSV. For each review a separated XML file is made in a specific folder for this edition in the folder /XML. In a general CSV file in /check_all_scrapes the review id of all scraped reviews is stored. Per new scrape the file is read, to prevent double scrapes. If for some reason new scraping of a particular edition is needed, you must first delete the id's of this particular edition in this list to be able to scrape again this edition.

3. When the general list of editions is long, it is foreseeable that the scraping will grind to a halt. (Sometimes it takes long for goodreads to respond, or a response is not there at all.) In this case use the command 'python scrape.py edition start [number]' to start the scraping again, to begin with the row in the list where the scraping halted. You can read in the screen output which row was being scraped when the scraping halted.

4. Goodreads only allows viewing the last 300 reviews. We did not find a way to bypass this limit. Its is however possible to scrape on 'language' and on 'star ratings' in Goodreads. This can be done also with this script. Use the command 'python scrape.py language' to scrape the reviews per language according to the Goodreads select option, or use 'python scrape.py stars' to scrape per star rating. The script will iterate and start with the 5 stars ratings, then the selenium browser will be refreshed, scrape the 4 star ratings and so on.

   The difficulty is however that also reviews from other editions are in the specified user language or specified star ratings.  These will overlap and double the scraped reviews per edition. This is the reason the scraping is done with different commands, so the per edition reviews are not polluted with double reviews. Although initially we hoped that new reviews would be generated, this appears not to be the case. The Goodreads filter can only be applied once: for 'this edition', or for  'review language' or for 'stars'. Combination will result, as explained, in added reviews from other editions.



### arguments

Arguments for scrape.py:

- 'makelist' (To be done first. To create an editions CSV with all the editions, and their individual urls that need to be scraped)

- 'edition [number]' (scrapes the edition of a book on a certain row of the editions CSV, ie.'scrape.py edition 12', scrapes the edition at row 12, row 1 is '1', not '0')

- 'edition all' (scrapes the whole list in a loop, starting from the first row. This will almost certainly grind to a halt with a long editions CSV, as the pushing of buttons with celenium is error prone)

- 'edition start [number]' (will start scraping and iterate starting from a specified row in the selected languages list, to be used when an error has occurred and the scraping needs to be started again.) ie. 'python scrape.py edition start 12', to start at row number 12 in the list.

- 'language' (will scrape on all review languages. But the reviews will target different editions, and if scraped are excluded from scraping again, so possibly not useful when reviews per edition are the research focus.) 

- 'stars' (will scrape per star rating. Will target all editions and overlap the edition scrapes, so possibly not useful if the focus is on reviews per edition)



