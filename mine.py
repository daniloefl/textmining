#!/usr/bin/env python

# coding: utf-8
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, similarities
import os
import utils

ntopics = 10       # number of topics to split the imput documents on
useLDA  = False    # whether to use Latent Dirichlet Allocation or LSI

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
  
  texts = []
  for doc in doc_set:
    raw = doc.lower() # to lower case
    tokens = tokenizer.tokenize(raw) # make word tokens and save it in a list
    lang_stop = set(stopwords.words('portuguese')) # get set of stop words for portuguese
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

  # now print the topics that appear often
  topics = myModel.print_topics()
  for i in range(0, len(topics)):
    print "Topic #%d: %s" %(i, topics[i]) # show it in the screen
    # make a graph showing this topic connected to its words, with the length
    # of the edge being the weight of the word in that topic
    utils.save_fulltopic_graph([ myModel.show_topics(ntopics, formatted=False)[i] ], [i], "_only_%d.html" % i)
  # same as before, but put all topics and words in the same graph
  utils.save_fulltopic_graph(myModel.show_topics(ntopics, formatted=False), range(0, len(topics)))

  # Try now projecting the document in the topics set
  # this tells us how much each topic contributes in a document
  print "Topics per document:"
  topic_per_doc = {}
  for did in range(0, len(texts)):
    if useLDA:
      print "Document %s: %s" % (doc_id[did], myModel.get_document_topics(tfidf[dictionary.doc2bow(texts[did])]))
    else:
      print "Document %s: %s" % (doc_id[did], myModel[tfidf[dictionary.doc2bow(texts[did])]])
    date = doc_id[did].split('/')[0]
    d = doc_id[did].split('/')[-1]
    if not date in topic_per_doc:
      topic_per_doc[date] = {}
    if useLDA:
      topic_per_doc[date][d] = myModel.get_document_topics(tfidf[dictionary.doc2bow(texts[did])])
    else:
      topic_per_doc[date][d] = myModel[tfidf[dictionary.doc2bow(texts[did])]]

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
  for did in range(0, len(texts)):
    similar[doc_id[did]] = {}
    for did2, weight in list(enumerate(index[topic_per_doc[date][d]])):
      similar[doc_id[did]][doc_id[did2]] = weight
  utils.save_similarity_graph(similar)

  # now try a similarity query for fixed date
  similar_date = {}
  for d in date_set: # for every date available
    texts_d = []
    did_d = []
    # for each document in that date
    for document in date_set[d]:
      texts_d.append(texts[document])
      did_d.append(doc_id[document])
    # train similarity model
    new_corpus = [dictionary.doc2bow(text) for text in texts_d]
    new_corpus_tfidf = tfidf[new_corpus] # apply the trained transformation to the corpus
    index_d = similarities.MatrixSimilarity(myModel[new_corpus_tfidf])
    similar_date[d] = {}
    for idx_id in range(0, len(did_d)):
      doc_name = did_d[idx_id].split('/')[-1]
      similar_date[d][doc_name] = {}
      for did2, weight in list(enumerate(index_d[ myModel[tfidf[dictionary.doc2bow(texts_d[idx_id])]] ])):
        doc_name2 = did_d[did2].split('/')[-1]
        similar_date[d][doc_name][doc_name2] = weight
    utils.save_similarity_graph(similar_date[d], "_%s.html" % d)
     
  # the following works, but it is too complicated
  # not easy to see anything
  # now make a graph of it
  # connecting the documents to topics
  # this is done for each document in a specific day
  #for date in topic_per_doc:
  #  # for all documents in this date
  #  utils.save_doctopic_graph(topic_per_doc[date], "topic_per_doc_%s.html" % date)
  #  utils.save_doctopic_full(topic_per_doc[date], myModel.show_topics(ntopics, formatted=False), "topic_per_doc_full_%s.html" % date)
  #  utils.save_doctopic_full_nointermediate(topic_per_doc[date], myModel.show_topics(ntopics, formatted=False), "topic_per_doc_full_nointermediate_%s.html" % date)
  #
  #utils.save_doc_word_time(topic_per_doc, ldamodel.show_topics(ntopics, formatted=False), ".html")

if __name__ == "__main__":
  main()
