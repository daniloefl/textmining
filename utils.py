#!/usr/bin/env python
# coding: utf-8

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
      s += v
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
      if "* Folha de S.Paulo" in line or re.match("^ *comente[ \n]*$", line):
        end = True
        continue
      if start and not end:
        if (not re.match(r"^ *Publicidade.*$", line)) and \
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
           (not re.match(r"^ *Escolha seu time.*$", line)) and \
           (not re.match(r"^ *Escolha seu signo.*$", line)) and \
           (not re.match(r"^ *Sua Folha[ \n]*$", line)) and \
           (not re.match(r"^.*Receber.*da Folha de S.Paulo\?[ \n]*$", line)) and \
           (not re.match(r"^ *Confirmar.*Cancelar[ \n]*$", line)) and \
           (not re.match(r"^ *Voce tambem gostaria de:[ \n]*$", line)) and \
           (not re.match(r"^ *Quais newsletters você gostaria de assinar\?[ \n]*$", line)) and \
           (not re.match(r"^ *Assine a Folha.*$", line)) and \
           (not re.match(r"^ *\[[ X]+\] .*$", line)) and \
           (not re.match(r"^ *[ _]+ enviar.*$", line)) and \
           (not re.match(r"^[ \n]*$", line)) and \
           (not re.match(r"^ *\w+[ \n]*$", line)): # only one word (start of section)
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
           (not re.match(r"^ *\w+[ \n]*$", line)): # only one word (start of section)
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
      if re.match("^ *Voce esta aqui:.*$", line) and not start:
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

