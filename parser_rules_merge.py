import ply.yacc as yacc
from lexer_rules import tokens

DEBUG = True

dicc = {}
consts = {}

#BNF

def p_start(p):
	'start : encabezado constantes voces'
	p[0] = p[1]
	print "expresion: " + str(p[0])

def p_encabezado(p):
	'encabezado : tempo compas'
	p[0] = p[1]
	print "encabezado"

def p_tempo(p):
	'tempo : HASH TEMPO FIGURE NUMBER'
	p[0] = {p[3]["type"] : p[4]}
	dicc["tempo"] = {p[3]["type"] : p[4]}
	print "tempo: " + str(p[0])

def p_compas(p):
	'compas : HASH COMPAS NUMBER DIV NUMBER'
	p[0] = str(p[3]) + "/" + str(p[5])
	dicc["compas"] = p[0]
	print "compas: " + p[0]

def p_constantes(p):
	'constantes : CONST CONSTID EQUAL NUMBER SEMICOLON constantes'
	consts[p[2]] = p[4]
	print "constantes: " + p[2] + ": " + str(consts[p[2]])

def p_constantes_lambda(p):
	'constantes : '
	pass

def p_voces(p):
	'voces : voz voces'

def p_voces_lambda(p):
	'voces : '
	pass

def p_voz(p):
    'voz : decla_instrumento LCURL musica RCURL'
    pass

def p_decla_instrumento(p):
    'decla_instrumento : VOICE LPAREN NUMBER RPAREN'
    pass

def p_decla_instrumento_const(p):
    'decla_instrumento : VOICE LPAREN CONSTID RPAREN'
    if(not(p[3] in consts)):
    	p_error(p)
    else:
    	pass

    pass

def p_musica_lambda(p):
    'musica :'
    pass

def p_musica_compas(p):
    'musica : compas musica'
    pass

def p_musica_bucle(p):
    'musica : bucle musica'
    pass

def p_compas(p):
    'compas : COMPAS LCURL notas RCURL'
    pass    

def p_bucle(p):
    'bucle : REPEAT LPAREN NUMBER RPAREN LCURL compas compases RCURL'
    pass    

def p_compases_lambda(p):
    'compases :'
    pass    

def p_compases(p):
    'compases : compas compases'
    pass

def p_notas_lambda(p):
    'notas : '
    pass    

def p_notas(p):
    'notas : figura notas'
    pass

def p_figura_nota(p):
    'figura : notaProd'
    pass

def p_figura_silencio(p):
    'figura : silencio'
    pass

def p_nota_prod(p):
    'notaProd : NOTA LPAREN altura COMMA NUMBER COMMA duracion RPAREN SEMICOLON'
    pass

def p_altura(p):
    'altura : FIGURE simbolo_altura'
    pass

def p_simbolo_altura_lambda(p):
    'simbolo_altura :'
    pass    

# def p_duracion_lambda(p):
#     'duracion :'
#     pass    

def p_duracion(p):
    'duracion : FIGURE'
    pass

# def p_duracion_punto(p):
#     'duracion : FIGURE DOT'
#     pass

def p_silencio(p):
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


parser = yacc.yacc()

s = ""
while True:
	try:
	    s = s + " " + raw_input()
	    if not(s):
    		continue
	except (EOFError):
		break

result = parser.parse(s)
print result