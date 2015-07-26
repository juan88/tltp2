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
    	p[0] = p[1]
        pass

    def p_encabezado(p):
    	'encabezado : tempo compas'
    	p[0] = p[1]
        pass

    def p_tempo(p):
    	'tempo : HASH TEMPO FIGURE NUMBER'
    	p[0] = {p[3]["type"] : p[4]}
    	Reglas.dicc["tempo"] = {p[3]["type"] : p[4]}
        pass

    def p_compas(p):
    	'compas : HASH COMPAS NUMBER DIV NUMBER'
    	p[0] = str(p[3]) + "/" + str(p[5])
    	Reglas.dicc["compas1"] = p[3]
        Reglas.dicc["compas2"] = p[5]
        Reglas.dicc["compas_val"] = (float(p[3]) / float(p[5]))
        pass

    def p_constantes(p):
    	'constantes : CONST CONSTID EQUAL NUMBER SEMICOLON constantes'
    	Reglas.consts[p[2]] = p[4]
        pass

    def p_constantes_lambda(p):
    	'constantes : '
    	pass

    def p_voces(p):
    	'voces : voz voces'
        pass

    def p_voces_lambda(p):
    	'voces : '
    	pass

    def p_voz(p):
        'voz : decla_instrumento LCURL musica RCURL'
        pass

    def p_decla_instrumento(p):
        'decla_instrumento : VOICE LPAREN NUMBER RPAREN'
        Reglas.cantvoices = Reglas.cantvoices + 1
        pass

    def p_decla_instrumento_const(p):
        'decla_instrumento : VOICE LPAREN CONSTID RPAREN'
        if(not(p[3] in Reglas.consts)):
        	message = "Constant " + p[3] + " not declared"
                raise Exception(message)
        else:
            Reglas.cantvoices = Reglas.cantvoices + 1

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

    def p_compas_def(p):
        'compas : COMPAS LCURL notas RCURL'
        if(p[3] != Reglas.dicc["compas_val"]):
            raise Exception("El tiempo del compas es erroneo")
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
        p[0] = 0
        return p

    def p_notas(p):
        'notas : figura notas'
        p[0] = p[1] + p[2]
        return p

    def p_figura_nota(p):
        'figura : notaProd'
        p[0] = p[1]
        return p

    def p_figura_silencio(p):
        'figura : silencio'
        p[0] = p[1]
        return p

    def p_nota_prod(p):
        'notaProd : NOTA LPAREN altura COMMA NUMBER COMMA duracion RPAREN SEMICOLON'
        p[0] = p[7]
        return p

# FALTA HACER QUE EN VEZ DE HACEPTAR UN NUMBER PUEDA ACEPTAR UN CONSTID
    def p_nota_prod_constid(p):
        'notaProd : NOTA LPAREN altura COMMA CONSTID COMMA duracion RPAREN SEMICOLON'
        if(not(p[5] in Reglas.consts)):
            message = "Constant " + p[5] + " not declared"
            raise Exception(message)
        else:
            p[0] = p[7]
        return p

    def p_altura(p):
        'altura : NOTAID simbolo_altura'
        pass

    def p_simbolo_altura_lambda(p):
        'simbolo_altura : '
        pass

    def p_simbolo_altura(p):
        'simbolo_altura : ALTURA'
        pass

    # def p_duracion_lambda(p):
    #     'duracion :'
    #     pass    

    def p_duracion(p):
        'duracion : FIGURE'
        p[0] = (float(1) / float(p[1]["value"]))
        return p

    def p_duracion_punto(p):
        'duracion : FIGURE DOT'
        p[0] = (1 / p[1]["value"]) * 1.5
        return p

    def p_silencio(p):
        'silencio : SILENCIO LPAREN duracion RPAREN SEMICOLON'
        p[0] = p[3]
        return p

    def p_error(token):
        message = "[Syntax error]"
        if token is not None:
            message += "\ntype:" + token.type
            message += "\nvalue:" + str(token.value)
            message += "\nline:" + str(token.lineno)
            message += "\nposition:" + str(token.lexpos) 
            raise Exception(message)

    yacc = yacc.yacc()
