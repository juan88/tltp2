import ply.yacc as yacc
from lexer_rules import tokens

DEBUG = True

dicc = {}
consts = {}

#BNF

def p_exp(p):
	'exp : encabezado'
	p[0] = p[1]
	print "expresion: " + str(p[0])

def p_encabezado(p):
	'encabezado : tempo compas const'
	p[0] = p[1]
	print "encabezado"

def p_tempo(p):
	'tempo : HASH TEMPO FIGURE NUMBER'
	p[0] = {p[3]["type"] : p[4]}
	dicc["tempo"] = p[0]
	print "tempo: " + str(p[0])

def p_compas(p):
	'compas : HASH COMPAS NUMBER DIV NUMBER'
	p[0] = str(p[3]) + "/" + str(p[5])
	dicc["compas"] = p[0]
	print "compas: " + p[0]

def p_const(p):
	'const : CONST CONSTID EQUAL NUMBER SEMICOLON const'
	consts[p[2]] = p[4]
	print "const: " + p[2] + ": " + str(consts[p[2]])

def p_const_nil(p):
	'const : '
	p[0] = None


def p_error(p):
	print "Tenes un error en ", p


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