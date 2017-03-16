
# coding: utf-8
wordMap = {
           "president": u"president|presidente",
           "dilma": u"Dilma",
           "temer": u"Temer",
           "oglobo": u"O Globo",
           "folha": u"Folha de SP",
           "bbc": u"BBC Brasil",
           "dw": u"DW Brasil",
           "carta": u"Carta Capital",
           "brasil": u"Brasil",
           "mulher": u"woman|mulher",
           "comissao": u"comission|comissão",
           "dia": u"day|dia",
           "nao": u"no|não",
           "impeach": u"impeachment",
           "processo": u"process|processo",
           "senado": u"Senate|Senado",
           "governo": u"government|governo",
           "trump": u"Trump",
           "desfil": u"parade|desfile",
           "rio": u"Rio",
           }

def showWord(w):
  if w in wordMap:
    return wordMap[w]
  return unicode(w)

