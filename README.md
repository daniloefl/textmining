# textmining

This downloads the front page of different Brazilian newspapers,
cleans them up, removing advertising and navigation bars, and
performs a topical text analysis using LDA or LSI.

This generates graphs showing how strongly related different documents
are connected.

It is configured to download four different news paper first pages:
O Globo, Folha da São Paulo, Deutsche Welle and BBC.
BBC and Deutsche Welle are downloaded in their Brazilian versions.

To run it, one must download each day their front page news using:

```
python get_data.py
```

The actual Lattent Dirichlet Allocation analysis is done with:

```
python mine.py
```

It produces an output HTML content that can be saved in a file and seen in a browser.
Take a look at some results in:
<https://daniloefl.github.io/textmining/results.html>

# Dependencies installation

```
$ sudo apt install python-nltk
$ python
>>> import nltk
>>> nltk.download()
(select corpora/stopwords)
>>> exit()
$ wget https://pypi.python.org/packages/72/91/d1a29c8ba866bed6c554a4039a842dd6fddc9bb78f335f3f9efd7dc9292e/gensim-1.0.0.tar.gz#md5=9dfccc8cb76d64c6ad18b628632d2e01
$ tar xvfz gensim-1.0.0.tar.gz
$ cd gensim-1.0.0
$ sudo python setup.py install
$ cd ..
$ sudo rm -rf gensim-1.0.0
$ sudo apt install wget lynx
$ sudo apt install python-pip
$ pip install bokeh
```

