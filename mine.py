
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


def save_fulltopic_graph(topics, fname = ".png"):
  import networkx as nx
  import matplotlib.pyplot as plt
  import matplotlib.gridspec as gridspec
  import math
  plt.figure(figsize=(10,10))
  G = nx.Graph()
  pos_fixed = {}
  center = []
  added_word = []
  node_topics = []
  node_words = []
  for t in range(0, len(topics)):
    G.add_node(t)
    node_topics.append(t)
    for word, weight in topics[t][1]:
      if not word in added_word:
        G.add_node(word)
        added_word.append(word)
        node_words.append(word)
      G.add_edge(t, word, weight = 500*weight, length=weight)
  pos=nx.spring_layout(G, weight = 'weight', scale = 10)
  nx.draw_networkx_nodes(G, pos, node_size=3000, nodelist=node_topics, node_color='g', alpha=0.8)
  nx.draw_networkx_nodes(G, pos, node_size=3000, nodelist=node_words, node_color='b', alpha=0.8)
  nx.draw_networkx_edges(G, pos, width=2, edge_color='r', alpha=0.5)
  #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
  #nx.draw(G, pos, node_size=5000, node_color='b', alpha=0.5, edge_color='r', width=2)
  nx.draw_networkx_labels(G,pos, font_size=10,font_family='sans-serif')
  plt.axis("off")
  plt.savefig("topic_all%s" % (fname))

def save_doctopic_graph(topics, fname = "doctopic_graph.png"):
  import networkx as nx
  import matplotlib.pyplot as plt
  plt.figure(figsize=(10,10))
  G = nx.Graph()
  added = []
  node_docs = []
  node_words = []
  for doc in topics:
    docname = doc
    t = topics[doc]
    G.add_node(docname)
    node_docs.append(docname)
    for word, weight in t:
      if not word in added:
        G.add_node(word)
        added.append(word)
        node_words.append(word)
      G.add_edge(docname, word, weight = 500*weight)
  pos=nx.spring_layout(G, scale=10) # positions for all nodes
  nx.draw_networkx_nodes(G,pos,node_size=3000, nodelist = node_docs, node_color='g', alpha=0.8)
  nx.draw_networkx_nodes(G,pos,node_size=3000, nodelist = node_words, node_color='b', alpha=0.8)
  nx.draw_networkx_edges(G, pos, width=2, edge_color='r', alpha=0.5)
  nx.draw_networkx_labels(G,pos,font_size=11,font_family='sans-serif')
  plt.axis("off")
  plt.savefig(fname)

def save_doctopic_full_nointermediate(doc_topics, topics, fname = "doctopic_graph.png"):
  import networkx as nx
  import matplotlib.pyplot as plt
  plt.figure(figsize=(20,20))
  G = nx.Graph()
  added_word = []
  node_docs = []
  node_words = []
  for doc in doc_topics:
    docname = doc
    t = doc_topics[doc]
    G.add_node(docname)
    node_docs.append(docname)
    for topic, weight in t:
      for word, weight_w in topics[topic][1]:
        if not word in added_word:
          G.add_node(word)
          added_word.append(word)
          node_words.append(word)
        G.add_edge(docname, word, weight = 500*weight_w*weight)
  pos=nx.spring_layout(G, scale=20) # positions for all nodes
  nx.draw_networkx_nodes(G,pos,node_size=3000, nodelist=node_docs, node_color='g', alpha=0.8)
  nx.draw_networkx_nodes(G,pos,node_size=3000, nodelist=node_words, node_color='b', alpha=0.8)
  nx.draw_networkx_edges(G, pos, width=2, edge_color='r', alpha=0.5)
  nx.draw_networkx_labels(G,pos,font_size=11,font_family='sans-serif')
  plt.axis("off")
  plt.savefig(fname)

def save_doctopic_full(doc_topics, topics, fname = "doctopic_graph.png"):
  import networkx as nx
  import matplotlib.pyplot as plt
  plt.figure(figsize=(20,20))
  G = nx.Graph()
  added = []
  added_word = []
  node_docs = []
  node_topics = []
  node_words = []
  for doc in doc_topics:
    docname = doc
    t = doc_topics[doc]
    G.add_node(docname)
    node_docs.append(docname)
    for topic, weight in t:
      if not topic in added:
        G.add_node(topic)
        added.append(topic)
        node_topics.append(topic)
        for word, weight_w in topics[topic][1]:
          if not word in added_word:
            G.add_node(word)
            added_word.append(word)
            node_words.append(word)
          G.add_edge(topic, word, weight = 500*weight_w)
      G.add_edge(docname, topic, weight = 500*weight)
  pos=nx.spring_layout(G, scale=20) # positions for all nodes
  nx.draw_networkx_nodes(G,pos,node_size=3000, nodelist=node_docs, node_color='r', alpha=0.8)
  nx.draw_networkx_nodes(G,pos,node_size=3000, nodelist=node_topics, node_color='g', alpha=0.8)
  nx.draw_networkx_nodes(G,pos,node_size=3000, nodelist=node_words, node_color='b', alpha=0.8)
  nx.draw_networkx_edges(G, pos, width=2, edge_color='r', alpha=0.5)
  nx.draw_networkx_labels(G,pos,font_size=11,font_family='sans-serif')
  plt.axis("off")
  plt.savefig(fname)

ldamodel = models.ldamodel.LdaModel(corpus, num_topics=5, id2word = dictionary, passes=1)
topics = ldamodel.print_topics(5)
for i in range(0, len(topics)):
  print "Topic #%d: %s" %(i, topics[i])
save_fulltopic_graph(ldamodel.show_topics(5, num_words=5, formatted=False))

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
  save_doctopic_graph(topic_per_doc[date], "topic_per_doc_%s.png" % date)
  save_doctopic_full(topic_per_doc[date], ldamodel.show_topics(5, num_words=5, formatted=False), "topic_per_doc_full_%s.png" % date)
  save_doctopic_full_nointermediate(topic_per_doc[date], ldamodel.show_topics(5, num_words=5, formatted=False), "topic_per_doc_full_nointermediate_%s.png" % date)

