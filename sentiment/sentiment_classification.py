import openpyxl
import pandas as pd

LANGUAGES = ['English', 'Dutch', 'French',
             'German', 'Italian', 'Portuguese', 'Spanish']


def create_dataframes(infile):
    wb = openpyxl.load_workbook(filename=infile)
    sheet_names = wb.sheetnames
    for lang in LANGUAGES:
        # find all sheets of the language, but don't use the non-annotated ones
        lang_sheets = [s for s in sheet_names if s.startswith(
            lang) and len(s) > len(lang)]
        out_df = pd.DataFrame()
        for i, key in enumerate(lang_sheets):
            sheet = wb[key]
            values = sheet.values
            df = pd.DataFrame(values, columns=next(values)).head(100)
            if i == 0:
                out_df['word'] = df['Word']
            out_df[key] = df.apply(
                lambda x: sentiment_classification(x['Category']), axis=1)
        out_df.to_csv('{}_ratings.csv'.format(lang), index=False)


def sentiment_classification(label):
    if not label:
        return None
    elif label.lower().startswith('p'):
        return 'P'
    elif label.lower().startswith('n'):
        return 'N'
    elif label.lower().startswith('h') or label.lower().startswith('c'):
        return 'H'
    else:
        return None
