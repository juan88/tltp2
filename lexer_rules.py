#Defino las palabras reservadas como key : value para asociarlas a un token
reservadas = {
  'tempo' : 'TEMPO',
  'voz' : 'VOICE',
  'const' : 'CONST',
  'nota' : 'NOTA',
  'silencio' : 'SILENCIO',
  'compas' : 'COMPAS',
  'repetir' : 'REPEAT',
}

# Todos los tokens que considero necesarios que me instancie el lexer
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


#Guardo un diccionario con una referencia de las figuras y su duración (esto lo usaré para guardar el valor de cada figura como un atributo)
figuras = {
  'redonda' : 1,
  'blanca' : 2,
  'negra' : 4,
  'corchea' : 8,
  'semicorchea' : 16,
  'fusa' : 32,
  'semifusa' : 64
  }

#Reglas para matchear los distintos tokens. El orden es importante en general
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


#ignoro whitespaces
t_ignore_WHITESPACES = r"[ \t]+"


#Mensaje de error de lexer genérico.
def t_error(token):
    message = " > Token desconocido:"
    message += "\ntype:" + token.type
    message += "\nvalue:" + str(token.value)
    message += "\nline:" + str(token.lineno)
    message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
