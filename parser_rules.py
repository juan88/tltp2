import ply.yacc as yacc
import sys
from parser import Parser
from lexer_rules import tokens

DEBUG = True

class Reglas():
    cantvoices = 1
    dicc = {}
    consts = {}


#BNF
    def p_start(p):
    	'start : encabezado constantes voces'
    	p[0] = [p[1], p[3]]

    def p_encabezado(p):
    	'encabezado : tempo compas'
    	p[0] = [p[1], p[2]]

    def p_tempo(p):
    	'tempo : HASH TEMPO FIGURE NUMBER'
    	p[0] = [p[3]["type"] , p[4]]

    def p_compas(p):
    	'compas : HASH COMPAS NUMBER DIV NUMBER'
    	p[0] = [p[3], p[5]]
        Reglas.dicc["compas_val"] = (float(p[3]) / float(p[5]))

    def p_constantes(p):
    	'constantes : CONST CONSTID EQUAL NUMBER SEMICOLON constantes'
    	Reglas.consts[p[2]] = p[4]

    def p_constantes_lambda(p):
    	'constantes : '

    def p_voces(p):
    	'voces : voz voces'
        p[0] = [p[1]] + p[2]

    def p_voces_lambda(p):
    	'voces : '
        p[0] = []

    def p_voz(p):
        'voz : decla_instrumento LCURL musica RCURL'
        p[0] = [p[1], p[3]]

    def p_decla_instrumento(p):
        'decla_instrumento : VOICE LPAREN NUMBER RPAREN'
        Reglas.cantvoices = Reglas.cantvoices + 1
        p[0] = p[3]

    def p_decla_instrumento_const(p):
        'decla_instrumento : VOICE LPAREN CONSTID RPAREN'
        if(not(p[3] in Reglas.consts)):
        	message = "Constant " + p[3] + " not declared"
                raise Exception(message)
        else:
            Reglas.cantvoices = Reglas.cantvoices + 1
            p[0] = Reglas.consts[p[3]]


    def p_musica_lambda(p):
        'musica :'
        p[0] = []

    def p_musica_compas(p):
        'musica : compas musica'
        p[0] = [['C', p[1]]] + p[2]

    def p_musica_bucle(p):
        'musica : bucle musica'
        p[0] = [['B', p[1]]] + p[2]

    def p_compas_def(p):
        'compas : COMPAS LCURL notas RCURL'
        lista = p[3]
        duracion_compas = 0
        for diccs in lista:
            duracion_compas += diccs["duration"]
        print duracion_compas
        if(duracion_compas != Reglas.dicc["compas_val"]):
            raise Exception("El tiempo del compas es erroneo")
        else:
            p[0] = lista

    def p_bucle(p):
        'bucle : REPEAT LPAREN NUMBER RPAREN LCURL musica RCURL'
        p[0] = [p[3], p[6]]


    def p_notas_lambda(p):
        'notas : '
        p[0] = []

    def p_notas(p):
        'notas : figura notas'
        p[0] = [p[1]] + p[2]

    def p_figura_nota(p):
        'figura : notaProd'
        p[0] = p[1]

    def p_figura_silencio(p):
        'figura : silencio'
        p[0] = p[1]

    def p_nota_prod(p):
        'notaProd : NOTA LPAREN altura COMMA NUMBER COMMA duracion RPAREN SEMICOLON'
        p[0] = {}
        p[0]["duration"] = p[7]
        p[0]["nota"] = p[3][0]
        p[0]["desv"] = p[3][1]
        p[0]["octava"] = p[5]
        p[0]["type"] = "NOT"

# FALTA HACER QUE EN VEZ DE HACEPTAR UN NUMBER PUEDA ACEPTAR UN CONSTID
    def p_nota_prod_constid(p):
        'notaProd : NOTA LPAREN altura COMMA CONSTID COMMA duracion RPAREN SEMICOLON'
        var = p[5]
        if(not(var in Reglas.consts)):
            message = "Constant " + var + " not declared"
            raise Exception(message)
        else:
            p[0] = {}
            p[0]["duration"] = p[7]
            p[0]["nota"] = p[3][0]
            p[0]["desv"] = p[3][1]
            p[0]["octava"] = Reglas.consts[var]
            p[0]["type"] = "NOT"

    def p_altura(p):
        'altura : NOTAID simbolo_altura'
        p[0] = [p[1], p[2]]

    def p_simbolo_altura_lambda(p):
        'simbolo_altura : '
        p[0] = ""

    def p_simbolo_altura(p):
        'simbolo_altura : ALTURA'
        p[0] = p[1]

    def p_duracion(p):
        'duracion : FIGURE'
        p[0] = (float(1) / float(p[1]["value"]))

    def p_duracion_punto(p):
        'duracion : FIGURE DOT'
        p[0] = (1 / float(p[1]["value"])) * 1.5

    def p_silencio(p):
        'silencio : SILENCIO LPAREN duracion RPAREN SEMICOLON'
        p[0] = {}
        p[0]["duration"] = p[3]
        p[0]["type"] = "SIL"

    def p_error(token):
        message = "[Syntax error]"
        if token is not None:
            message += "\ntype:" + token.type
            message += "\nvalue:" + str(token.value)
            message += "\nline:" + str(token.lineno)
            message += "\nposition:" + str(token.lexpos) 
        
        raise Exception(message)

    yacc = yacc.yacc()
