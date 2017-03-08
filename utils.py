#!/usr/bin/env python
# coding: utf-8

from presentation import showWord

import re
import codecs

class Source(object):
  def __init__(self, www, language='pt'):
    self.www = www
    self.language = language
  def clean(self, filename, outfile):
    f = codecs.open(filename, encoding='utf-8', mode='r')
    o = codecs.open(outfile, encoding='utf-8', mode='w')
    for line in f:
      o.write(line)
    o.close()
    f.close()
  def remove_symbols(self, line):
    s = ""
    for c in range(0, len(line)):
      v = line[c]
      if v == u'á': v = 'a'
      if v == u'é': v = 'e'
      if v == u'í': v = 'i'
      if v == u'ó': v = 'o'
      if v == u'ú': v = 'u'
      if v == u'Á': v = 'A'
      if v == u'É': v = 'E'
      if v == u'Í': v = 'I'
      if v == u'Ó': v = 'O'
      if v == u'Ú': v = 'U'
      if v == u'ü': v = 'u'
      if v == u'Ü': v = 'U'
      if v == u'â': v = 'a'
      if v == u'ê': v = 'e'
      if v == u'ô': v = 'o'
      if v == u'Â': v = 'A'
      if v == u'Ê': v = 'E'
      if v == u'Ô': v = 'O'
      if v == u'ç': v = 'c'
      if v == u'Ç': v = 'C'
      if v == u'ã': v = 'a'
      if v == u'õ': v = 'o'
      if v == u'Ã': v = 'A'
      if v == u'Õ': v = 'O'
      if v == u'à': v = 'a'
      if v == u'‘': v = ''
      if v == u'’': v = ''
      if v == u'\'': v = ''
      if v == u'?': v = ' '
      if v == u'!': v = ' '
      if v == u',': v = ' '
      if v == u'.': v = ' '
      if v == u':': v = ' '
      if v == u'"': v = ' '
      if v == u'”': v = ' '
      if v == u'“': v = ' '
      if v == u'ñ': v = 'n'
      if v == u'à': v = 'a'
      if v == u'À': v = 'A'
      s += v
    s.replace('AI-5','AI5')
    s.replace('ai-5','ai5')
    return s

class BBCSource(Source):
  def __init__(self, www, language='pt'):
    super(BBCSource, self).__init__(www, language)
  def clean(self, filename, outfile):
    f = codecs.open(filename, encoding='utf-8', mode='r')
    o = codecs.open(outfile, encoding='utf-8', mode='w')
    start = False
    end = False
    for line in f:
      line = self.remove_symbols(line)
      if "Principais noticias" in line:
        start = True
        continue
      if "BBC Brasil nas redes sociais" in line:
        end = True
        continue
      if start and not end:
        if (not re.match(r"^ *Video[ \n]*$", line)) and \
           (not re.match(r"^ *Destaques e Analises[ \n]*$", line)) and \
           (not re.match(r"^ *Principais noticias[ \n]*$", line)) and \
           (not re.match(r"^ *Brasil[ \n]*$", line)) and \
           (not re.match(r"^ *\* [0-9]+ [\w]+ [0-9]+.*$", line)) and \
           (not re.match(r"^ *Que duvida de portugues mais te confunde?.*[ \n]*$", line)) and \
           (not re.match(r"^ *BBC Brasil respondera duvidas sobre saque do FGTS.*[ \n]*$", line)) and \
           (not re.match(r"^[ \n]*$", line)) and \
           (not re.match(r"^ *\w+[ \n]*$", line)): # only one word (start of section)
          o.write(line)
    o.close()
    f.close()

class FolhaSource(Source):
  def __init__(self, www, language='pt'):
    super(FolhaSource, self).__init__(www, language)
  def clean(self, filename, outfile):
    f = codecs.open(filename, encoding='utf-8', mode='r')
    o = codecs.open(outfile, encoding='utf-8', mode='w')
    start = False
    end = False
    for line in f:
      line = self.remove_symbols(line)
      if " buscar" in line:
        start = True
        continue
      if "* Folha de S.Paulo" in line or re.match("^ *comente[ \n]*$", line) or re.match("^ *Folha Internacional[ \n]*$", line):
        end = True
        continue
      if start and not end:
        if (not re.match(r"^ *Publicidade.*$", line)) and \
           (not re.match(r"^ *Atualizado em .*$", line)) and \
           (not re.match(r"^ *Bovespa[ \+\-0-9\(\)h%R\$]*$", line)) and \
           (not re.match(r"^ *Dolar Com[ \+\-0-9\(\)h%R\$]*$", line)) and \
           (not re.match(r"^ *Euro[ \+\-0-9\(\)h%R\$]*$", line)) and \
           (not re.match(r"^ *\* \+ Lidas[ \n]*$", line)) and \
           (not re.match(r"^ *\* \+ Comentadas[ \n]*$", line)) and \
           (not re.match(r"^ *\* \+ Enviadas[ \n]*$", line)) and \
           (not re.match(r"^ *\* Ultimas[ \n]*$", line)) and \
           (not re.match(r"^ *\* English[ \n]*$", line)) and \
           (not re.match(r"^ *\* Espanol[ \n]*$", line)) and \
           (not re.match(r"^ *[0-9]+  Item.*$", line)) and \
           (not re.match(r"^ *Escolha um colunista[ \n]*$", line)) and \
           (not re.match(r"^ *Personalize[ \n]*$", line)) and \
           (not re.match(r"^ *Configuracoes[ \n]*$", line)) and \
           (not re.match(r"^ *escolha 2 itens.*$", line)) and \
           (not re.match(r"^ *Escolha um .*$", line)) and \
           (not re.match(r"^ *Painel do Leitor.[ \n]*$", line)) and \
           (not re.match(r"^ *Escolha seu time.*$", line)) and \
           (not re.match(r"^ *Escolha seu signo.*$", line)) and \
           (not re.match(r"^ *CLOVIS ROSSI[ \n]*$", line)) and \
           (not re.match(r"^ *SEU BOLSO[ \n]*$", line)) and \
           (not re.match(r"^ *Sua Folha[ \n]*$", line)) and \
           (not re.match(r"^ *\*[ \n]*$", line)) and \
           (not re.match(r"^.*Receber.*da Folha de S.Paulo\?[ \n]*$", line)) and \
           (not re.match(r"^ *Confirmar.*Cancelar[ \n]*$", line)) and \
           (not re.match(r"^ *Voce tambem gostaria de:[ \n]*$", line)) and \
           (not re.match(r"^ *Quais newsletters você gostaria de assinar\?[ \n]*$", line)) and \
           (not re.match(r"^ *Assine a Folha.*$", line)) and \
           (not re.match(r"^ *\[[ X]+\] .*$", line)) and \
           (not re.match(r"^ *[ _]+ enviar.*$", line)) and \
           (not re.match(r"^[ \n]*$", line)) and \
           (not re.match(r"^ *\w+[ \n]*$", line)): # only one word (start of section)
          line = line.replace("Reproducao/TV Globo", "")
          s = line.find(u" –")
          if s > 0:
            line = line[0:s]
          o.write(line)
    o.close()
    f.close()

class OGloboSource(Source):
  def __init__(self, www, language='pt'):
    super(OGloboSource, self).__init__(www, language)
  def clean(self, filename, outfile):
    f = codecs.open(filename, encoding='utf-8', mode='r')
    o = codecs.open(outfile, encoding='utf-8', mode='w')
    start = False
    end = False
    for l in f:
      line = self.remove_symbols(l)
      if (re.match("^\w.*$", line) and ("Ir para a pagina" not in line) and ("Assuntos em Destaque" not in line)) \
          and not start:
        start = True
        continue
      if ("* Topicos" in line or re.match("^Newsletter[ \n]$", line)) and start:
        end = True
        continue
      if start and not end:
        if (not re.match(r"^ *Publicidade.*$", line)) and \
           (not re.match(r"^[ \n]*$", line)) and \
           (not re.match(r"^ *\+[ \n]*$", line)) and \
           (not re.match(r"^ *Anterior Proximo[ \n]*$", line)) and \
           (not re.match(r"^ *[0-9]+ de [0-9]+[ \n]*$", line)) and \
           (not re.match(r"^ *Page Not Found[ \n]*$", line)) and \
           (not re.match(r"^ *\w+[ \n]*$", line)): # only one word (start of section)
          for k in [" / O GLOBO", " / O Globo", " / Agencia O Globo", "Agencia O Globo", "O Globo", "O GLOBO"]:
            s = line.find(k)
            if s >= 0:
              line = line[0:s]
            break
          o.write(line)
    o.close()
    f.close()

class CartaSource(Source):
  def __init__(self, www, language='pt'):
    super(CartaSource, self).__init__(www, language)
  def clean(self, filename, outfile):
    f = codecs.open(filename, encoding='utf-8', mode='r')
    o = codecs.open(outfile, encoding='utf-8', mode='w')
    start = False
    end = False
    for line in f:
      line = self.remove_symbols(line)
      if re.match("^ *Voce esta aqui.*$", line) and not start:
        start = True
        continue
      if re.match(r"^ *Carta Capital[ \n]*$", line) and start:
        end = True
        continue
      if start and not end:
        if (not re.match(r"^ *Publicidade.*$", line)) and \
           (not re.match(r"^[ _]*Assinar.*$", line)) and \
           (not re.match(r"^ *Mais.*$", line)) and \
           (not re.match(r"^ *Newsletter.*$", line)) and \
           (not re.match(r"^ *Novidades da CartaCapital.*$", line)) and \
           (not re.match(r"^ *IFRAME:[ \n]*$", line)) and \
           (not re.match(r"^ *\*[ \n]*$", line)) and \
           (not re.match(r"^ *Dolar comercial[ \+0-9R\$%\n]*$", line)) and \
           (not re.match(r"^ *Dolar paralelo[ \+0-9R\$%\n]*$", line)) and \
           (not re.match(r"^ *Euro[ \+0-9R\$%\n]*$", line)) and \
           (not re.match(r"^ *Bovespa[ \+0-9R\$%\n]*$", line)) and \
           (not re.match(r"^ *Nasdaq[ \+0-9R\$%\n]*$", line)) and \
           (not re.match(r"^ *Frankfurt[ \+0-9R\$%\n]*$", line)) and \
           (not re.match(r"^ *Atualizacao[ 0-9/]* as [ 0-9\n]*$", line)) and \
           (not re.match(r"^ *Fonte  CMA[ \n]*$", line)) and \
           (not re.match(r"^.*http.*mercadoconfianca.*$", line)) and \
           (not re.match(r"^[ \n]*$", line)) and \
           (not re.match(r"^ *\w+[ \n]*$", line)): # only one word (start of section)
          o.write(line)
    o.close()
    f.close()

class DWSource(Source):
  def __init__(self, www, language='pt'):
    super(DWSource, self).__init__(www, language)
  def clean(self, filename, outfile):
    f = codecs.open(filename, encoding='utf-8', mode='r')
    o = codecs.open(outfile, encoding='utf-8', mode='w')
    start = False
    end = False
    for line in f:
      line = self.remove_symbols(line)
      if re.match("^ *NOTICIAS / .*$", line) and not start:
        start = True
        continue
      if re.match(r"^Compartilhar[ \n]*$", line) and start:
        end = True
        continue
      if start and not end:
        if (not re.match(r"^ *Publicidade.*$", line)) and \
           (not re.match(r"^ *Feedback.*$", line)) and \
           (not re.match(r"^ *\* default[ \n]*$", line)) and \
           (not re.match(r"^ *\* .*$", line)) and \
           (not re.match(r"^ *Autoria .*$", line)) and \
           (not re.match(r"^ *\[\][ \n]*$", line)) and \
           (not re.match(r"^ *Mais[ \n]*$", line)) and \
           (not re.match(r"^ *Assistir ao video.*$", line)) and \
           (not re.match(r"^[ \n]*$", line)) and \
           (not re.match(r"^ *\w+[ \n]*$", line)): # only one word (start of section)
          o.write(line)
    o.close()
    f.close()
    
sources = {
           'oglobo': OGloboSource('http://oglobo.globo.com/'),
           'folha':  FolhaSource('http://www.folha.uol.com.br/'),
           'carta':  CartaSource('https://www.cartacapital.com.br/'),
           'bbc':    BBCSource('http://www.bbc.com/portuguese/brasil'),
           'dw':     DWSource('http://www.dw.com/pt-br/not%C3%ADcias/brasil/s-7142'),
          }



def save_fulltopic_graph(topics, fname = ".png"):
  import networkx as nx
  import matplotlib.pyplot as plt
  import matplotlib.gridspec as gridspec
  import math
  fig = plt.figure(figsize=(10,10))
  G = nx.Graph()
  pos_fixed = {}
  center = []
  added_word = []
  node_topics = []
  node_words = []
  for t in range(0, len(topics)):
    G.add_node(showWord(t))
    node_topics.append(showWord(t))
    for word, weight in topics[t][1]:
      if not word in added_word:
        G.add_node(showWord(word))
        added_word.append(word)
        node_words.append(showWord(word))
      G.add_edge(showWord(t), showWord(word), weight = 500*weight, length=weight)
  pos=nx.spring_layout(G, weight = 'weight', scale = 10)
  nx.draw_networkx_nodes(G, pos, node_size=3000, nodelist=node_topics, node_color='g', alpha=0.8)
  nx.draw_networkx_nodes(G, pos, node_size=3000, nodelist=node_words, node_color='b', alpha=0.8)
  nx.draw_networkx_edges(G, pos, width=2, edge_color='r', alpha=0.5)
  #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
  #nx.draw(G, pos, node_size=5000, node_color='b', alpha=0.5, edge_color='r', width=2)
  nx.draw_networkx_labels(G,pos, font_size=10,font_family='sans-serif')
  plt.axis("off")
  plt.savefig("topic_all%s" % (fname))
  plt.close(fig)

def save_doctopic_graph(topics, fname = "doctopic_graph.png"):
  import networkx as nx
  import matplotlib.pyplot as plt
  fig = plt.figure(figsize=(10,10))
  G = nx.Graph()
  added = []
  node_docs = []
  node_words = []
  for doc in topics:
    docname = doc
    t = topics[doc]
    G.add_node(showWord(docname))
    node_docs.append(showWord(docname))
    for word, weight in t:
      if not word in added:
        G.add_node(showWord(word))
        added.append(word)
        node_words.append(showWord(word))
      G.add_edge(showWord(docname), showWord(word), weight = 500*weight)
  pos=nx.spring_layout(G, scale=10) # positions for all nodes
  nx.draw_networkx_nodes(G,pos,node_size=3000, nodelist = node_docs, node_color='g', alpha=0.8)
  nx.draw_networkx_nodes(G,pos,node_size=3000, nodelist = node_words, node_color='b', alpha=0.8)
  nx.draw_networkx_edges(G, pos, width=2, edge_color='r', alpha=0.5)
  nx.draw_networkx_labels(G,pos,font_size=11,font_family='sans-serif')
  plt.axis("off")
  plt.savefig(fname)
  plt.close(fig)

def save_doctopic_full_nointermediate(doc_topics, topics, fname = "doctopic_graph.png"):
  import networkx as nx
  import matplotlib.pyplot as plt
  fig = plt.figure(figsize=(20,20))
  G = nx.Graph()
  added_word = []
  node_docs = []
  node_words = []
  for doc in doc_topics:
    docname = doc
    t = doc_topics[doc]
    G.add_node(showWord(docname))
    node_docs.append(showWord(docname))
    for topic, weight in t:
      for word, weight_w in topics[topic][1]:
        if not word in added_word:
          G.add_node(showWord(word))
          added_word.append(word)
          node_words.append(showWord(word))
        G.add_edge(showWord(docname), showWord(word), weight = 500*weight_w*weight)
  pos=nx.spring_layout(G, scale=20) # positions for all nodes
  nx.draw_networkx_nodes(G,pos,node_size=3000, nodelist=node_docs, node_color='g', alpha=0.8)
  nx.draw_networkx_nodes(G,pos,node_size=3000, nodelist=node_words, node_color='b', alpha=0.8)
  nx.draw_networkx_edges(G, pos, width=2, edge_color='r', alpha=0.5)
  nx.draw_networkx_labels(G,pos,font_size=11,font_family='sans-serif')
  plt.axis("off")
  plt.savefig(fname)
  plt.close(fig)

def save_doctopic_full(doc_topics, topics, fname = "doctopic_graph.png"):
  import networkx as nx
  import matplotlib.pyplot as plt
  fig = plt.figure(figsize=(20,20))
  G = nx.Graph()
  added = []
  added_word = []
  node_docs = []
  node_topics = []
  node_words = []
  for doc in doc_topics:
    docname = doc
    t = doc_topics[doc]
    G.add_node(showWord(docname))
    node_docs.append(showWord(docname))
    for topic, weight in t:
      if not topic in added:
        G.add_node(showWord(topic))
        added.append(topic)
        node_topics.append(showWord(topic))
        for word, weight_w in topics[topic][1]:
          if not word in added_word:
            G.add_node(showWord(word))
            added_word.append(word)
            node_words.append(showWord(word))
          G.add_edge(showWord(topic), showWord(word), weight = 500*weight_w)
      G.add_edge(showWord(docname), showWord(topic), weight = 500*weight)
  pos=nx.spring_layout(G, scale=20) # positions for all nodes
  nx.draw_networkx_nodes(G,pos,node_size=3000, nodelist=node_docs, node_color='r', alpha=0.8)
  nx.draw_networkx_nodes(G,pos,node_size=3000, nodelist=node_topics, node_color='g', alpha=0.8)
  nx.draw_networkx_nodes(G,pos,node_size=3000, nodelist=node_words, node_color='b', alpha=0.8)
  nx.draw_networkx_edges(G, pos, width=2, edge_color='r', alpha=0.5)
  nx.draw_networkx_labels(G,pos,font_size=11,font_family='sans-serif')
  plt.axis("off")
  plt.savefig(fname)
  plt.close(fig)

def save_doc_word_time(docs, topics, fname = ".png"):
  import matplotlib.pyplot as plt
  import datetime
  from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
  from numpy import arange
  x = [0]*len(docs.keys())
  y = {}
  word_list = []
  date_id = 0
  for date in docs:
    x[date_id] = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
    for doc in docs[date]:
      docname = doc
      if not docname in y:
        y[docname] = {}
      t = docs[date][doc]
      for topic, weight in t:
        for word, weight_w in topics[topic][1]:
          if not word in word_list:
            word_list.append(word)
          if not word in y[docname]:
            y[docname][word] = [0]*len(docs)
          y[docname][word][date_id] = weight*weight_w
    date_id += 1
  
  for word in word_list:
    fig, ax = plt.subplots()
    count = 0
    ls = ['-', '--', '-.', ':', '-', '--', '-.', ':']
    lc = ['b', 'b', 'b', 'b', 'r', 'r', 'r', 'r']
    for docname in y:
      if not word in y[docname]: continue
      plt.plot_date(x, y[docname][word], label=docname, linewidth=2, linestyle = ls[count], color=lc[count])
      count += 1
    plt.legend(loc="upper left")
    plt.xlabel("Date")
    plt.ylabel("Probability")
    ax.set_xlim(x[0], x[-1])

    ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%d/%m/%Y'))
    ax.fmt_xdata = DateFormatter('%d/%m/%Y')
    fig.autofmt_xdate()

    ax.grid(True)
    plt.savefig("pertime_%s%s" % (word, fname))
    plt.close(fig)
