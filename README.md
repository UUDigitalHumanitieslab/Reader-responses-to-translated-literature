# Reader responses to translated literature

This repository contains code for the [DIOPTRA-L](https://cdh.uu.nl/portfolio/digital-opinions-on-translated-literature-dioptra-l-2/) project by Haidee Kotze, Gys-Walt van Egdom, Corina Koolen and Utrecht University's Research Software Lab, and can be used to reproduce the publication

Kotze, Haidee & Janssen, Berit & Koolen, Corina & Plas, Luka & Egdom, Gys-Walt. (2021). _Norms, affect and evaluation in the reception of literary translations in multilingual online reading communities: Deriving cognitive-evaluative templates from big data._ Translation, Cognition & Behavior. 4. 10.1075/tcb.00060.kot.

## Prerequisites
### Python
Most of the scripts require Python 3.6. To install dependencies, run
`pip install -r requirements.txt`

### R
The statistical analysis and visualization was performed in R, using the following libraries:
- coin
- dplyr
- ggplot2
- Hmisc
- irr
- lme4
- reshape2
- rstatix

## Steps to reproduce
1. scrapers: Python scripts used to scrape reviews from Goodreads. Documentation on usage in that folder's README.
2. preprocessing: Python scripts used to clean the data, and more specifically, tokenization.
3. embeddings: Jupyter notebooks for training and evaluating word embeddings using word2vec. As the dataset is relatively small, the resulting embeddings were not informative for further research.
4. analysis: Python scripts to collect and count translation lemmas, based on human annotations.
5. collocations: Python scripts for finding collocations surrounding translation lemmas
6. sentiment: Python scripts to count positive / negative and hedge terms in collocations.
7. model: R scripts used to generate statistics and visualizations of the data.

