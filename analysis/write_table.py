# write table with 1 row per mention of translation

import pandas as pd
from analysis.count_data import count_data

reviews_path = './data/goodreads_tokenised.csv'
export_path = './data/goodreads_formatted.csv'

data = count_data(reviews_path)
data.to_csv(export_path)