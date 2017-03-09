
# coding: utf-8
wordMap = {
           "president": u"president\npresidente",
           "dilma": u"Dilma",
           "temer": u"Temer",
           "oglobo": u"O Globo",
           "folha": u"Folha de S. Paulo",
           "bbc": u"BBC Brasil",
           "dw": u"DW Brasil",
           "carta": u"Carta Capital",
           "brasil": u"Brasil",
           "mulher": u"woman\nmulher",
           "comissao": u"comission\ncomissão",
           "dia": u"day\ndia",
           "nao": u"no\nnão",
           "impeach": u"impeachment",
           "processo": u"process\nprocesso",
           }

def showWord(w):
  if w in wordMap:
    return wordMap[w]
  return w

