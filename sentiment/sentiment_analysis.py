from transformers import pipeline
import pandas as pd
from os.path import isfile

languages = ['English', 'Dutch', 'German', 'French', 'Italian', 'Spanish']
selected_columns = ['id', 'language', 'rating_no', 'sentiment']
out_csv = 'reviews_sentiment_text.csv'

def analyze_sentiment(review_file):
    reviews = pd.read_csv(review_file)
    start_from = None
    data = reviews[(reviews['text'].notna()) & (reviews['language'].isin(languages))].sample(10000, random_state=21)
    data['sentiment'] = data.apply(lambda x: sentiment_classification(x['rating_no']), axis=1)
    classifier = pipeline('sentiment-analysis', model="nlptown/bert-base-multilingual-uncased-sentiment")
    if isfile(out_csv):
        done_records = pd.read_csv(out_csv)
        start_from = len(done_records.index)
    for i, row in data.iterrows():
        write_header = True if i==0 else False
        output = pd.DataFrame.from_dict({key: [row[key]] for key in selected_columns})
        if start_from:
            if i < start_from:
                continue
        try:
            analysis = classifier(row['tokenised_text'][:512])
            output['prediction'] = int(analysis[0]['label'][:1])
        except:
            output['prediction'] = None
        
        output.to_csv(out_csv, mode='a', header=write_header, index=False)

def sentiment_classification(rating_no):
    if rating_no >= 4:
        sentiment = 'P'
    elif rating_no <= 2:
        sentiment = 'N'
    else:
        sentiment = '-'
    return sentiment

def calculate_accuracy(sentiment_file=out_csv):
    data = pd.read_csv(sentiment_file)
    data['pred_sentiment'] = data.apply(lambda x: sentiment_classification(x['prediction']), axis=1)
    data['diff'] = abs(data['rating_no']-data['prediction'])
    print('percentage exact label correct: ', len(data[data['rating_no']==data['prediction']])/len(data))
    print('percentage sentiment label correct: ', len(data[data['sentiment']==data['pred_sentiment']])/len(data))
    print('one off accuracy: ', len(data[data['diff']<2])/len(data))

"""
exact: 0.34
correct category: 0.53
one-off: 0.64
"""

"""
Full text scores (sample of 10000 reviews)
percentage exact label correct:  0.3316
percentage sentiment label correct:  0.5308
one off accuracy:  0.6458
"""