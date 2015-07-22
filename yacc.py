import ply.yacc as yacc
from lexer_rules import tokens

DEBUG = True

name = {}

#BNF

def p_exp(p):
	'exp : encabezado'
	p[0] = p[1]
	print "expresion: " + str(p[0])

def p_encabezado(p):
	'encabezado : tempo compas'
	p[0] = p[1]
	print "encabezado"

def p_tempo(p):
	'tempo : HASH TEMPO FIGURE NUMBER'
	p[0] = p[3]
	print "tempo: " + str(p[0])

def p_tempo_nil(p):
	'tempo : NIL'
	print "tempo nil"

def p_compas(p):
	'compas : HASH COMPAS NUMBER DIV NUMBER'
	p[0] = p[3]
	print "compas"

def p_compas_nil(p):
	'compas : NIL'
	print "compas es nil"

def p_error(p):
	print "Tenes un error en ", p


parser = yacc.yacc()

for tok in tokens:
	print tok

while True:
    s = raw_input("musileng > ")
    if not(s):
        continue
    result = parser.parse(s)
    print result
