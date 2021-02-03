# write table with 1 row per review

import pandas as pd
from analysis.count_data import count_data_per_review

reviews_path = './data/goodreads_tokenised.csv'
export_path = './data/goodreads_review_data.csv'

data = count_data_per_review(reviews_path)
data.to_csv(export_path)