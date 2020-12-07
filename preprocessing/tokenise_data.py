import csv
from preprocessing.tokeniser import Tokeniser

REVIEWS_FILE = './data/reviews_about_translation.csv'
LANGUAGE = 'english'

with open(REVIEWS_FILE) as infile:
    outpath = REVIEWS_FILE[:-4] + '_tokenised.csv'
    with open(outpath, 'w') as outfile:
        reader = csv.DictReader(infile)
        fieldnames_in = reader.fieldnames

        fieldnames_out = fieldnames_in + ['tokenised_text']
        writer = csv.DictWriter(outfile, fieldnames_out)
        writer.writeheader()

        t = Tokeniser(LANGUAGE)

        for row in reader:
            text = row['text'] 
            tokens = t.process(text)
            tokenised_text = ' '.join(tokens)
            row['tokenised_text'] = tokenised_text
            writer.writerow(row)
