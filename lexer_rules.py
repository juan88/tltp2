reservadas = {
  'tempo' : 'TEMPO',
  'voz' : 'VOICE',
  'const' : 'CONST',
  'nota' : 'NOTA',
  'silencio' : 'SILENCIO',
  'compas' : 'COMPAS',
  'repetir' : 'REPEAT',
}

tokens = [
   'HASH',
   'NUMBER',
   'FIGURE',
   'LCURL',
   'RCURL',
   'RPAREN',
   'LPAREN',
   'DIV',
   'SEMICOLON',
   'EQUAL',
   'ALTURA',
   'CONSTID'
] + list(reservadas.values())


figuras = {
  'redonda' : 1,
  'blanca' : 2,
  'negra' : 4,
  'corchea' : 8,
  'semicorchea' : 16,
  'fusa' : 32,
  'semifusa' : 64
  }

def t_NUMBER(token):
  r"[1-9][0-9]*|0"
  token.value = int(token.value)
  return token

def t_FIGURE(token):
  r"redonda|blanca|negra|corchea|semicorchea|fusa|semifusa"
  if token.value in figuras:
    token.value = {"value": figuras[token.value], "type": token.value}
  return token


def t_CONSTID(token):
  r"[_a-zA-Z]+"
  #print token.value + ' -> ' + reservadas.get(token.value, 'CONSTID')
  token.type = reservadas.get(token.value, 'CONSTID')
  return token

def t_NEWLINE(token):
  r"\n+"
  token.lexer.lineno += len(token.value)

def t_ignore_COMMENT(t):
  r'//.*'
  pass


t_ALTURA = r"[\+\-]"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LCURL = r"{"
t_RCURL = r"}"
t_DIV = r"/"
t_HASH = r"\#"
t_SEMICOLON = r";"
t_EQUAL = r"="


#ignoro whitespaces y comentarios?
t_ignore_WHITESPACES = r"[ \t]+"


def t_error(token):
    message = " > Token desconocido:"
    message += "\ntype:" + token.type
    message += "\nvalue:" + str(token.value)
    message += "\nline:" + str(token.lineno)
    message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
