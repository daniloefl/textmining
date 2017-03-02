
import re

class Source(object):
  def __init__(self, www, language='pt'):
    self.www = www
    self.language = language
  def clean(self, filename, outfile):
    f = open(filename, 'r')
    o = open(outfile, 'w')
    for line in f:
      o.write(line)
    o.close()
    f.close()

class BBCSource(Source):
  def __init__(self, www, language='pt'):
    super().__init__(www, language)
  def clean(self, filename, outfile):
    f = open(filename, 'r')
    o = open(outfile, 'w')
    start = False
    end = False
    for line in f:
      if "Principais notícias" in line:
        start = True
        continue
      if "BBC Brasil nas redes sociais" in line:
        end = True
        continue
      if start and not end:
        if (not re.match(r"^ *Vídeo[ \n]*$", line)) and
           (not re.match(r"^ *Destaques e Análises[ \n]*$", line)) and
           (not re.match(r"^ *Principais notícias[ \n]*$", line)) and
           (not re.match(r"^ *Brasil[ \n]*$", line)) and
           (not re.match(r"^ *\* [0-9]+ \w+ [0-9]+.*$", line)) and
           (not re.match(r"^ *Que dúvida de português mais te confunde?.*[ \n]*$", line)) and
           (not re.match(r"^ *BBC Brasil responderá dúvidas sobre saque do FGTS.*[ \n]*$", line)) and
           (not re.match(r"^[ \n]*$", line)):
          o.write(line)
    o.close()
    f.close()

class FolhaSource(Source):
  def __init__(self, www, language='pt'):
    super().__init__(www, language)
  def clean(self, filename, outfile):
    f = open(filename, 'r')
    o = open(outfile, 'w')
    start = False
    end = False
    for line in f:
      if " buscar" in line:
        start = True
        continue
      if "* Folha de S.Paulo" in line:
        end = True
        continue
      if start and not end:
        if (not re.match(r"^ *Publicidade.*$", line)) and
           (not re.match(r"^ *\* \+ Lidas[ \n]*$", line)) and
           (not re.match(r"^ *\* \+ Comentadas[ \n]*$", line)) and
           (not re.match(r"^ *\* \+ Enviadas[ \n]*$", line)) and
           (not re.match(r"^ *\* Últimas[ \n]*$", line)) and
           (not re.match(r"^ *\* English[ \n]*$", line)) and
           (not re.match(r"^ *\* Español[ \n]*$", line)) and
           (not re.match(r"^ *Escolha um colunista[ \n]*$", line)) and
           (not re.match(r"^ *Personalize[ \n]*$", line)) and
           (not re.match(r"^ *Configurações[ \n]*$", line)) and
           (not re.match(r"^ *escolha 2 itens.*$", line)) and
           (not re.match(r"^ *Escolha um .*$", line)) and
           (not re.match(r"^ *Escolha seu time.*$", line)) and
           (not re.match(r"^ *Escolha seu signo.*$", line)) and
           (not re.match(r"^ *Sua Folha[ \n]*$", line)) and
           (not re.match(r"^.*Receber.*da Folha de S.Paulo\?[ \n]*$", line)) and
           (not re.match(r"^ *Confirmar.*Cancelar[ \n]*$", line)) and
           (not re.match(r"^ *Você também gostaria de:[ \n]*$", line)) and
           (not re.match(r"^ *Quais newsletters você gostaria de assinar\?[ \n]*$", line)) and
           (not re.match(r"^ *Assine a Folha.*$", line)) and
           (not re.match(r"^ *\[[ X]+\] .*$", line)) and
           (not re.match(r"^ *[ _]+ enviar.*$", line)) and
           (not re.match(r"^[ \n\*]*$", line)):
          o.write(line)
    o.close()
    f.close()

class OGloboSource(Source):
  def __init__(self, www, language='pt'):
    super().__init__(www, language)
  def clean(self, filename, outfile):
    f = open(filename, 'r')
    o = open(outfile, 'w')
    start = False
    end = False
    for line in f:
      if (re.match("^ *Lava-Jato[ \n]$", line) or
          re.match("^ *Brasil[ \n]$", line) or
          re.match("^ *Família[ \n]$", line) or
          re.match("^ *Economia[ \n]$", line) or
          re.match("^ *Sociedade[ \n]$", line) or
          re.match("^ *Mundo[ \n]$", line) or
          re.match("^ *Rio[ \n]$", line) or
          re.match("^ *Boa viagem[ \n]$", line)
         )
          and not start:
        start = True
        continue
      if "* Tópicos" in line:
        end = True
        continue
      if start and not end:
        if (not re.match(r"^ *Publicidade.*$", line)) and
           (not re.match(r"^[ \n\*\+]*$", line)):
          o.write(line)
    o.close()
    f.close()

class CartaSource(Source):
  def __init__(self, www, language='pt'):
    super().__init__(www, language)
  def clean(self, filename, outfile):
    f = open(filename, 'r')
    o = open(outfile, 'w')
    start = False
    end = False
    for line in f:
      if re.match("^ *Você está aqui:.*$", line) and not start:
        start = True
        continue
      if re.match(r"^ *Carta Capital[ \n]*$", line) and start:
        end = True
        continue
      if start and not end:
        if (not re.match(r"^ *Publicidade.*$", line)) and
           (not re.match(r"^[ _]*Assinar.*$", line)) and
           (not re.match(r"^ *Novidades da CartaCapital.*$", line)) and
           (not re.match(r"^ *IFRAME[ \n]*$", line)) and
           (not re.match(r"^[ \n\*\+_]*$", line)):
          o.write(line)
    o.close()
    f.close()

class DWSource(Source):
  def __init__(self, www, language='pt'):
    super().__init__(www, language)
  def clean(self, filename, outfile):
    f = open(filename, 'r')
    o = open(outfile, 'w')
    start = False
    end = False
    for line in f:
      if re.match("^ *NOTÍCIAS / .*$", line) and not start:
        start = True
        continue
      if re.match(r"^ *Ver mais[ \n]*$", line) and start:
        end = True
        continue
      if start and not end:
        if (not re.match(r"^ *Publicidade.*$", line)) and
           (not re.match(r"^[ \n\*\+_]*$", line)):
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

