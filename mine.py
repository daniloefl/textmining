
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

ldamodel = models.ldamodel.LdaModel(corpus, num_topics=5, id2word = dictionary, passes=1)
topics = ldamodel.print_topics(5)
for i in range(0, len(topics)):
  print "Topic #%d: %s" %(i, topics[i])
utils.save_fulltopic_graph(ldamodel.show_topics(5, num_words=5, formatted=False))

print "--"
print "Topics per document:"
topic_per_doc = {}
for did in range(0, len(texts)):
  print "Document %s: %s" % (doc_id[did], ldamodel.get_document_topics(dictionary.doc2bow(texts[did])))
  date = doc_id[did].split('/')[0]
  d = doc_id[did].split('/')[-1]
  if not date in topic_per_doc:
    topic_per_doc[date] = {}
  topic_per_doc[date][d] = ldamodel.get_document_topics(dictionary.doc2bow(texts[did]))
for date in topic_per_doc:
  utils.save_doctopic_graph(topic_per_doc[date], "topic_per_doc_%s.png" % date)
  utils.save_doctopic_full(topic_per_doc[date], ldamodel.show_topics(5, num_words=5, formatted=False), "topic_per_doc_full_%s.png" % date)
  utils.save_doctopic_full_nointermediate(topic_per_doc[date], ldamodel.show_topics(5, num_words=5, formatted=False), "topic_per_doc_full_nointermediate_%s.png" % date)

utils.save_doc_word_time(topic_per_doc, ldamodel.show_topics(5, num_words=5, formatted=False), ".png")
