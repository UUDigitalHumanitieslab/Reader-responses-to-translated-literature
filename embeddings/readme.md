English embeddings for goodreads reviews.

Setup for a python 3.6 environment:
```bash
pip install gensim==3.8
pip install nltk
python -m train.download
```
The train.download module downloads the Brown corpus for pretraining and a question-answer dataset for evaluation. The reviews have to be downloaded manually from I-analyzer. 

Embeddings can be trained from the command line:
```bash
python -m train
```
There are no command line options, so edit `train/__main__.py` to configure hyperparameters.

To evaluate:
```bash
python -m eval
```
Check that the code in `eval/__main__.py` uses the right embeddings.


For the visualisation of results:
Setup with
```bas
pip install jupyter
pip install matplotlib
pip install sklearn
```

Open `visualise/plot.ipynb` as a jupyter notebook.