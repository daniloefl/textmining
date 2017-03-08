
wordMap = {
           "president": "president\npresidente",
           "dilma": "Dilma",
           "temer": "Temer",
           "oglobo": "O Globo",
           "folha": "Folha de S. Paulo",
           "bbc": "BBC Brasil",
           "dw": "DW Brasil",
           "carta": "Carta Capital",
           "brasil": "Brasil",
           "mulher": "woman\nmulher",
           "comissao": "comission\ncomissão",
           "dia": "day\ndia",
           "nao": "no\nnão",
           "impeach": "impeachment",
           }

def showWord(w):
  if w in wordMap:
    return wordMap[w]
  return w

