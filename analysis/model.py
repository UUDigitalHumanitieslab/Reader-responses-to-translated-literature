from analysis.count_data import count_data

reviews_path = './data/reviews_about_translation_tokenised.csv'

data = count_data(reviews_path)
print(data.describe())