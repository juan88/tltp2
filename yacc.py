import ply.yacc as yacc
from lex import tokens

DEBUG = True

name = {}

#BNF

def p_exp(p):
	'exp : encabezado'
	p[0] = p[1]

def p_encabezado(p):
	'encabezado : tempo compas'
	p[0] = p[1] + p[2]

def p_tempo(p):
	'tempo : HASH FIGURE NUMBER'
	p[0] = p[2]

def p_compas(p):
	'compas : HASH COMPAS NUMBER DIV NUMBER'

def p_error(p):
	print "Error en ", p


yacc.yacc()