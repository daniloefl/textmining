
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import os
import utils

doc_set = []
doc_id = []
for day in os.listdir('data/'):
  for s in utils.sources:
    source = utils.sources[s]
    output = 'data/%s/%s' % (day, s)
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
  lang_stop.add("diz")
  lang_stop.add("folhapress")
  lang_stop.add("agencia")
  lang_stop.add("globo")
  lang_stop.add("foto")
  lang_stop.add("2017")
  lang_stop.add("sao")
  lang_stop.add("veja")
  lang_stop.add("kim")
  lang_stop.add("maxson")
  lang_stop.add("hugh")
  lang_stop.add("sobr")
  lang_stop.add("vai")
  lang_stop.add("passa")
  lang_stop.add("ano")
  lang_stop.add("rs")
  lang_stop.add("ser")
  lang_stop.add("morar")
  stopped_tokens = [i for i in tokens if not i in lang_stop]

  # stem token
  text = [p_stemmer.stem(i) for i in stopped_tokens]
  texts.append(text)

#print texts
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

ldamodel = models.ldamodel.LdaModel(corpus, num_topics=10, id2word = dictionary, passes=1)
topics = ldamodel.print_topics(10, 10)
for i in range(0, len(topics)):
  print "Topic #%d: %s" %(i+1, topics[i])


