from collocations.collocations import collocate

languages_patterns = {
    'dutch' :  r'^vertaa?l',
    'english' : r'^translat',
    'french' : r'^tradu',
    'german' : r'[uü]bersetz',
    'italian' : r'^tradu',
    'portuguese' : r'^tradu',
    'spanish' : r'^tradu',
}

for language, pattern in languages_patterns.items():
    if pattern:
        collocate(language, pattern)