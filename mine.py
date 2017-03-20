#!/usr/bin/env python

# coding: utf-8
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import os
import utils

ntopics = 20

def main():
  doc_set = []
  doc_id = []
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
  
  tokenizer = RegexpTokenizer(r'\w+')
  
  # Create p_stemmer of class PorterStemmer
  p_stemmer = PorterStemmer()
  
  texts = []
  for doc in doc_set:
    raw = doc.lower()
    tokens = tokenizer.tokenize(raw)
    lang_stop = set(stopwords.words('portuguese'))
    stopped_tokens = [i for i in tokens if not i in lang_stop]
  
    # stem token
    text = [p_stemmer.stem(i) for i in stopped_tokens]
    texts.append(text)
  
  #print texts
  dictionary = corpora.Dictionary(texts)
  corpus = [dictionary.doc2bow(text) for text in texts]
  
  #ldamodel = models.ldamodel.LdaModel(corpus, num_topics=ntopics, id2word = dictionary)
  ldamodel = models.lsimodel.LsiModel(corpus, num_topics=ntopics, id2word = dictionary)
  topics = ldamodel.print_topics()
  for i in range(0, len(topics)):
    print "Topic #%d: %s" %(i, topics[i])
    utils.save_fulltopic_graph([ ldamodel.show_topics(ntopics, formatted=False)[i] ], [i], "_only_%d.html" % i)
  utils.save_fulltopic_graph(ldamodel.show_topics(ntopics, formatted=False), range(0, len(topics)))
  
  print "--"
  print "Topics per document:"
  topic_per_doc = {}
  for did in range(0, len(texts)):
    if hasattr(ldamodel, "get_document_topics"):
      print "Document %s: %s" % (doc_id[did], ldamodel.get_document_topics(dictionary.doc2bow(texts[did])))
    else:
      print "Document %s: %s" % (doc_id[did], ldamodel[dictionary.doc2bow(texts[did])])
    date = doc_id[did].split('/')[0]
    d = doc_id[did].split('/')[-1]
    if not date in topic_per_doc:
      topic_per_doc[date] = {}
    if hasattr(ldamodel, "get_document_topics"):
      topic_per_doc[date][d] = ldamodel.get_document_topics(dictionary.doc2bow(texts[did]))
    else:
      topic_per_doc[date][d] = ldamodel[dictionary.doc2bow(texts[did])]
  for date in topic_per_doc:
    utils.save_doctopic_graph(topic_per_doc[date], "topic_per_doc_%s.html" % date)
    utils.save_doctopic_full(topic_per_doc[date], ldamodel.show_topics(ntopics, formatted=False), "topic_per_doc_full_%s.html" % date)
    utils.save_doctopic_full_nointermediate(topic_per_doc[date], ldamodel.show_topics(ntopics, formatted=False), "topic_per_doc_full_nointermediate_%s.html" % date)
  
  utils.save_doc_word_time(topic_per_doc, ldamodel.show_topics(ntopics, formatted=False), ".html")

if __name__ == "__main__":
  main()
