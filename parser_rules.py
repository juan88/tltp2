from lexer_rules import tokens
from traductor import *

def p_start(subexpressions):
    'start : encabezado constantes voces'
    subexpressions[0] = Traductor(subexpressions[1], subexpressions[2], subexpressions[3])

def p_encabezado(subexpressions):
    'encabezado : tempo compas_def'
    subexpressions[0] = Encabezado(subexpressions[1], subexpressions[2])

def p_tempo(subexpressions):
    'tempo : HASH TEMPO FIGURE NUMBER'
    subexpressions[0] = True

def p_compas_def(subexpressions):
    'compas_def : HASH COMPAS NUMBER DIV NUMBER'
    pass

def p_constantes_lambda(subexpressions):
    'constantes :'
    pass

def p_constantes(subexpressions):
    'constantes : CONST CONSTID EQUAL NUMBER SEMICOLON constantes'
    pass

def p_voces(subexpressions):
    'voces : decla_instrumento LCURL musica RCURL'
    pass

def p_decla_instrumento(subexpressions):
    'decla_instrumento : VOICE LPAREN NUMBER RPAREN'
    pass

def p_musica_lambda(subexpressions):
    'musica :'
    pass

def p_musica_compas(subexpressions):
    'musica : compas musica'
    pass

def p_musica_bucle(subexpressions):
    'musica : bucle musica'
    pass

def p_compas(subexpressions):
    'compas : COMPAS LCURL notas RCURL'
    pass    

def p_bucle(subexpressions):
    'bucle : REPEAT LPAREN NUMBER RPAREN LCURL compas compases RCURL'
    pass    

def p_compases_lambda(subexpressions):
    'compases :'
    pass    

def p_compases(subexpressions):
    'compases : compas compases'
    pass

def p_notas_lambda(subexpressions):
    'notas :'
    pass    

def p_notas(subexpressions):
    'notas : figura notas'
    pass

def p_figura_nota(subexpressions):
    'figura : NOTAID'
    pass

def p_figura_silencio(subexpressions):
    'figura : silencio'
    pass

def p_nota(subexpressions):
    'nota : NOTA LPAREN altura COMMA NUMBER COMMA duracion RPAREN'
    pass

def p_altura(subexpressions):
    'altura : FIGURE simbolo_altura'
    pass

def p_simbolo_altura_lambda(subexpressions):
    'simbolo_altura :'
    pass    

def p_duracion_lambda(subexpressions):
    'duracion :'
    pass    

def p_duracion(subexpressions):
    'duracion : FIGURE'
    pass

def p_duracion_punto(subexpressions):
    'duracion : FIGURE DOT'
    pass

def p_silencio(subexpressions):
    'silencio : SILENCIO LPAREN duracion RPAREN'
    pass

def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
        raise Exception(message)
