import csv
from preprocessing.tokeniser import Tokeniser

REVIEWS_FILE = './data/reviews_dutch.csv'

with open(REVIEWS_FILE) as infile:
    outpath = REVIEWS_FILE[:-4] + '_tokenised.csv'
    with open(outpath, 'w') as outfile:
        reader = csv.DictReader(infile)
        fieldnames_in = reader.fieldnames

        fieldnames_out = fieldnames_in + ['tokenised_text']
        writer = csv.DictWriter(outfile, fieldnames_out)
        writer.writeheader()

        tokenisers = {}
        available_languages = Tokeniser.available_languages()

        for row in reader:    
            #check language and initialise tokeniser if needed
            language = row['language'].lower()
            if language in tokenisers:
                t = tokenisers[language]
            elif language in available_languages:
                t = Tokeniser(language)
                tokenisers[language] = t
            else:
                t = None

            #if there is a tokeniser...
            if t:
                #process the review
                text = row['text'] 
                tokens = t.process(text)
                tokenised_text = ' '.join(tokens)
                
                #write
                row['tokenised_text'] = tokenised_text
                writer.writerow(row)
