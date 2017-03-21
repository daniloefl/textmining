#!/usr/bin/env python

# coding: utf-8
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, similarities
import os
import utils
import datetime

ntopics   = 4        # number of topics to split the imput documents on
useLDA    = True     # whether to use Latent Dirichlet Allocation or LSI

# words to query in documents
sim_query = ['Impeachment golpe', 'democracia brasil',
             'Violacoes de direitos humanos',
             'Aumento em casos de febre amarela',
             'Temer',
             'Dilma',
             'inflacao',
             'saude']

def main():

  # first of all transform HTML into plain text
  # to remove all the HTML tags
  # then use the clean() function of the Source class
  # to clean up rubbish (ie: navigation bars, advertisement)
  # the document is stored in data/[date]/[source tag]/frond_clean.txt
  # the document's clean text is in doc_set and its date and source are kept with
  # the same index in doc_id
  doc_set = []
  doc_id = []
  date_set = {}
  dirlist = os.listdir('data/')
  dirlist.sort()
  for day in dirlist:
    for s in utils.sources:
      source = utils.sources[s]
      output = 'data/%s/%s' % (day, s)
      os.system('lynx -dump -nolist %s/front.html > %s/front.txt' % (output, output))
      source.clean('%s/front.txt' %output, '%s/front_clean.txt' % output)
      f = open("%s/front_clean.txt" % output)
      doc = ""
      for i in f.readlines(): doc += i
      doc_set.append(doc)
      doc_id.append('%s/%s' % (day, s))
      if not day in date_set: date_set[day] = []
      date_set[day].append(len(doc_id)-1)

  # now we need to split it into words
  # and remove the word ending, so that only the stem of the word remains
  # this removes differences between masculin and feminin and plural/singular
  # we also remove common articles, prepositions, etc, which happen too often and carry no
  # meaning in the "bad-of-words" approach
  tokenizer = RegexpTokenizer(r'\w+')
  
  # Create p_stemmer of class PorterStemmer
  p_stemmer = PorterStemmer()

  # stop words
  lang_stop = (stopwords.words('portuguese')) # get set of stop words for portuguese
  lang_stop.extend(['bbc', 'globo', 'foto', 'agencia', 'photo', '01', '00', 'folha', 'folhapress'])
  
  texts = []
  for doc in doc_set:
    raw = doc.lower() # to lower case
    tokens = tokenizer.tokenize(raw) # make word tokens and save it in a list
    stopped_tokens = [i for i in tokens if not i in lang_stop] # remove stop words
  
    # stem token
    text = [p_stemmer.stem(i) for i in stopped_tokens]
    texts.append(text) # texts keeps a list of list of words (same indexing as doc_set and doc_id)
  
  # now make a dictionary of words found
  # this assigns a unique integer to each word
  dictionary = corpora.Dictionary(texts)
  # we can use dictionary.token2id to get the list of word-id mapping
  # doc2bow counts how many times a word appears in the text and makes a list of counts of words
  # this is now closer to a vector interpretation of each document
  corpus = [dictionary.doc2bow(text) for text in texts]
  # we would now like to use the tf-idf transformation for each document representation
  # this weights more words that appear very often, but normalises it by the size of the document
  # to avoid biases to large documents
  # it also underweights terms that appears to often in many documents
  # this avoids the appearance of wors such as "say", which often appears in newspapers
  tfidf = models.TfidfModel(corpus, normalize = True)
  corpus_tfidf = tfidf[corpus] # apply the trained transformation to the corpus
  
  # now make the model, which can be LSI for an SVD transformation of the 
  # term-document matrix
  # or LDA for a probabilistic model
  if useLDA:
    myModel = models.ldamodel.LdaModel(corpus_tfidf, num_topics=ntopics, id2word = dictionary)
  else:
    myModel = models.lsimodel.LsiModel(corpus_tfidf, num_topics=ntopics, id2word = dictionary)

  print "<!DOCTYPE html>"
  print "<html lang=\"en\"><head>"
  print """
<meta charset="utf-8">
<link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-0.12.4.min.css" type="text/css" />
        
<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-0.12.4.min.js"></script>
<script type="text/javascript">
    Bokeh.set_log_level("info");
</script>
        <style>
          body {
            margin: auto;
            text-align: left;
            text-weight: bold;
            font-size: 1.2em;
          }
          table, th, td {
            padding: 0.5em;
            text-align: center;
          }
          th {
            height: 2em;
            font-size: 1.4em;
          }
          th, td {
            border-bottom: 1px solid #ddd;
          }
          tr:hover {
            background-color: #f5f5f5;
          }
          table {
            padding-right: 1em;
            padding-left: 1em;
            border-collapse: collapse;
            width: 100%;
          }
        </style>
"""
  print "<title>Results of text mining Brazilian newspapers front page</title></head><body><h3>Results of text mining Brazilian newspapers front page</h3>"

  # now print the topics that appear often
  topics = myModel.show_topics(ntopics, formatted=False)
  for i in range(0, len(topics)):
    print "<table>"
    print "<tr><th colspan=\"2\">Words within topic '%d':</th></tr>" % i
    print "<tr><th>Contribution</th><th>Word</th></tr>"
    for v in topics[i][1]:
      print "<tr><td>%6.4f</td><td>%10s</td></tr>" % (v[1], utils.showWord(v[0]))
    print "</table>"

    # make a graph showing this topic connected to its words, with the length
    # of the edge being the weight of the word in that topic
    utils.save_fulltopic_graph([ myModel.show_topics(ntopics, formatted=False)[i] ], [i], "_only_%d.html" % i)
  # same as before, but put all topics and words in the same graph
  script, div = utils.save_fulltopic_graph(myModel.show_topics(ntopics, formatted=False), range(0, len(topics)))
  print "<h4>Graph showing words in each topic</h4>"
  print script
  print div

  # Try now projecting the document in the topics set
  # this tells us how much each topic contributes in a document
  print "Topics per document:"
  topic_per_doc = {}
  for did in range(0, len(texts)):
    print "<table>"
    date = doc_id[did].split('/')[0]
    dt = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
    print "<tr><th colspan=\"2\">Topics within document '%s' of '%s':</th></tr>" % (utils.showWord(doc_id[did].split('/')[-1]), dt.date())
    print "<tr><th>Relevance</th><th>Topic</th></tr>"
    if useLDA:
      topics = myModel.get_document_topics(tfidf[dictionary.doc2bow(texts[did])])
    else:
      topics = myModel[tfidf[dictionary.doc2bow(texts[did])]]
    for k,v in topics:
      print "<tr><td>%6.4f</td><td>%d</td></tr>" % (v, k)
    print "</table>"
    date = doc_id[did].split('/')[0]
    d = doc_id[did].split('/')[-1]
    if not date in topic_per_doc:
      topic_per_doc[date] = {}
    topic_per_doc[date][d] = topics

  # now make a graph of it
  # connecting the documents to topics
  # this is done for each document in a specific day
  for date in topic_per_doc:
    # for all documents in this date
    script, div = utils.save_doctopic_graph(topic_per_doc[date], "topic_per_doc_%s.html" % date)
    dt = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
    print "<h4>Graph showing topics in each document at %s</h4>" % dt.date()
    print script
    print div
  #  utils.save_doctopic_full(topic_per_doc[date], myModel.show_topics(ntopics, formatted=False), "topic_per_doc_full_%s.html" % date)
  #  utils.save_doctopic_full_nointermediate(topic_per_doc[date], myModel.show_topics(ntopics, formatted=False), "topic_per_doc_full_nointermediate_%s.html" % date)
  #
  #utils.save_doc_word_time(topic_per_doc, ldamodel.show_topics(ntopics, formatted=False), ".html")

  # now do a similarity query
  if useLDA:
    corpus_projection = myModel.get_document_topics(corpus_tfidf)
  else:
    corpus_projection = myModel[corpus_tfidf]
  index = similarities.MatrixSimilarity(corpus_projection)

  # we can now use index[input], where input = myModel[tfidf[dictionary.doc2bow(newDocument.lower().split())]]
  # this compares a new document with what is in the corpus
  # we can compare the documents in the corpus with each other
  similar = {}
  for item in sim_query:
    similar[item] = []
    if useLDA:
      result = myModel.get_document_topics(tfidf[ dictionary.doc2bow([p_stemmer.stem(i) for i in tokenizer.tokenize(item.lower()) if not i in lang_stop]) ])
    else:
      result = myModel[ tfidf[ dictionary.doc2bow([p_stemmer.stem(i) for i in tokenizer.tokenize(item.lower()) if not i in lang_stop]) ] ]
    for did2, weight in list(enumerate( index[ result ] )):
      similar[item].append((weight, doc_id[did2]))

  for item in sim_query:
    print "<table>"
    print "<tr><th colspan=\"3\">Documents matching '%s':</th></tr>" % item
    print "<tr><th>Similarity (%)</th><th>Source</th><th>Date</th></tr>"
    for k,v in sorted(similar[item], key=lambda val: -val[0]):
      date = v.split('/')[0]
      dt = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
      print "<tr><td>%5.2f</td><td>%20s</td><td>%20s</td></tr>" % (k*100, utils.showWord(v.split('/')[-1]), dt.date())
    print "</table>"

  print "</body></html>"

if __name__ == "__main__":
  main()
