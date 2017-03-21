
# coding: utf-8
wordMap = {
           "doria": u"Dória",
           "economia": u"economy|economia",
           "alckmin": u"Alckmin",
           "mandava": u"order|mandar",
           "atriz": u"actress|atriz",
           "juca": u"Jucá",
           "bela": u"beautiful|bela",
           "transposicao": u"transposition|transposição",
           "aborto": u"abortion|aborto",
           "professor": u"teacher|professor",
           "caixao": u"coffin|caixão",
           "iraquiana": u"Iraqi|iraquiana",
           "carregam": u"carry|carregam",
           "gato": u"cat|gato",
           "pombo": u"pigeon|pombo",
           "garfield": u"Garfield",
           "marinalva": u"Marinalva",
           "estadio": u"stadium|estádio",
           "amazonica": u"Amazônica",
           "rara": u"rare|rara",
           "relatam": u"tell|relatam",
           "detroit": u"Detroit",
           "nobr": u"noble|nobre",
           "seita": u"cult|seita",
           "filgueira": u"Filgueira",
           "peruana": u"Peruvian|peruana",
           "acompanh": u"accompany|acompanhar",
           "deserto": u"desert|deserto",
           "parcial": u"partial|parcial",
           "macri": u"Macri",
           "trecho": u"part|trecho",
           "metro": u"subway|metrô",
           "sean": u"Sean",
           "natal": u"Christmas|Natal",
           "onca": u"jaguar|onça",
           "bolsonaro": u"Bolsonaro",
           "barack": u"Barack",
           "morador": u"dweller|morador",
           "berco": u"crib|berço",
           "ruth": u"Ruth",
           "kit": u"kit",
           "zibaldoni": u"Zibaldoni",
           "sediar": u"to host|sediar",
           "escravo": u"slave|escravo",
           "vale": u"worth|vale",
           "viver": u"to live|viver",
           "pussi": u"Pussy",
           "riot": u"Riot",
           "berri": u"Berry",
           "fila": u"queue|fila",
           "criam": u"to create|criar",
           "enfrentam": u"to confront|enfrentar",
           "onibu": u"bus|ônibus",
           "aluno": u"student|aluno",
           "respond": u"to answer|responder",
           "relato": u"story|relato",
           "paralisacao": u"strike|paralisação",
           "samba": u"Samba|samba",
           "habib": u"Habib",
           "depressao": u"depression|depressão",
           "espaci": u"space|espaço",
           "droga": u"drug|droga",
           "pergunta": u"question|pergunta",
           "promet": u"promise|prometer",
           "fronteira": u"border|fronteira",
           "mae": u"mother|mãe",
           "veta": u"veto|vetar",
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
           "reproducao": u"reproduction|reprodução",
           "amarela": u"yellow|amarela",
           "morr": u"die|morrer",
           "febr": u"fever|febre",
           "preve": u"foresee|prever",
           "chuck": u"Chuck",
           "cronologia": u"cronology|cronologia",
           "votacao": u"vote|votação",
           "mandato": u"mandate|mandato",
           "concluiram": u"concluded|concluíram",
           "mal": u"bad|mal",
           "carn": u"meat|carne",
           "luxo": u"luxury|luxo",
           "palacio": u"palace|palácio",
           "presidenci": u"presidency|presidência",
           "destituida": u"destituted|destituída",
           "escandalo": u"scandal|escândalo",
           "reproducao": u"reproduction|reprodução",
           "fraca": u"weak|fraca",
           "faz": u"to do|fazer",
           "cidadania": u"citizenship|cidadania",
           "mora": u"to live|morar",
           "humano": u"human|humano",
           "aprend": u"to learn|aprender",
           "parda": u"brown|parda",
           "catadora": u"picker|catadora",
           "perderam": u"lost|perderam",
           "camara": u"chamber|camara",
           "expo": u"expose|expôr",
           "travesti": u"transvestite|travesti",
           "dandara": u"Dandara",
           "achaqu": u"achaque",
           "sp": u"São Paulo",
           "evitar": u"avoid|evitar",
           "uber": u"Uber",
           "tragedia": u"tragedy|tragédia",
           "cubatao": u"Cubatão",
           "siria": u"Siria|Síria",
           "holanda": u"Neatherlands|Holanda",
           "viagem": u"travel|viagem",
           "ana": u"Ana",
           "facebook": u"Facebook",
           "divulgacao": u"marketing|divulgação",
           "ar": u"air|ar",
           "curriculo": u"curriculum|currículo",
           }

def showWord(w):
  if w in wordMap:
    return wordMap[w].encode('utf-8')
  if isinstance(w, str):
    return w.encode('utf-8')
  return w

