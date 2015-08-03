import ply.yacc as yacc
import sys
from parser import Parser
from lexer_rules import tokens

DEBUG = True


#Clase propia para manejar los errores de Musileng
class SemanticException(Exception):
    def __init__(self, message, lineNumber):

        # Call the base class constructor with the parameters it needs
        #super(MusilengException, self).__init__(message)

        # Now for your custom code...
        self.message = message
        self.lineNumber = lineNumber
        self.filename = ''
        Reglas.cantvoices = 1
        Reglas.dicc = {}
        Reglas.consts = {}
        Reglas.constsCon = {}

    def __str__(self):
        return self.errorMsg()    

    def errorMsg(self):
        """ Muestro un mesaje custom de error diciendo en que archivo, nro de linea y error que hubo """
        return " --> " + self.filename + ":" + str(self.lineNumber) + " - " + self.message

class Reglas():
    cantvoices = 1
    dicc = {}
    consts = {}
    constsCon = {}

    @classmethod
    def instrumentoEnRango(cls, idInstrumento):
        """ Devuelve True si un instrumento esta bien configurado en el rango aceptado por MIDI """
        return idInstrumento >= 0 and idInstrumento <= 127

    @classmethod
    def octavaEnRango(cls, octava):
        """ Chequeo que el valor de la octava este bien definido """
        return octava >= 1 and octava <= 9


#BNF
    def p_start(p):
    	'start : encabezado constantes voces'
        Reglas.cantvoices = 1
        Reglas.dicc = {}
        Reglas.consts = {}
        Reglas.constsCon = {}
        v = p[3]
        p[2] = []
    	p[0] = [p[1][1], v]
        if(len(v) == 0 or len(v) > 16):
            raise SemanticException("La cantidad de voces debe ser mayor a cero", p.lineno(3))

    def p_encabezado(p):
    	'encabezado : tempo compas'
    	p[0] = ["encabezado", [p[1], p[2]]]


    def p_tempo(p):
    	'tempo : HASH TEMPO FIGURE NUMBER'
        tempo = p[4]
        if tempo <= 0:
            raise SemanticException("El tiempo de duracion de la figura "+ str(p[3]["type"]) +" debe ser mayor a 0.", p.lineno(3))
    	p[0] = [p[3]["type"] , tempo]

    def p_compas(p):
    	'compas : HASH COMPAS NUMBER DIV NUMBER'
    	p[0] = [p[3], p[5]]
        Reglas.dicc["compas_val"] = (float(p[3]) / float(p[5]))

    def p_constantes(p):
    	'constantes : CONST CONSTID EQUAL NUMBER SEMICOLON constantes'
        heredated = Reglas.consts.keys()
        con = p[2]
        if(con in heredated):
            message = "Constant " + con + " has already been declared"
            raise SemanticException(message, p.lineno(2))
    	Reglas.consts[con] = p[4]
        prev = p[-1][0]
        if prev == "encabezado":
            for current in Reglas.constsCon.keys():
                if Reglas.constsCon[current][0] in Reglas.consts.keys():
                    Reglas.consts[current] = Reglas.consts[Reglas.constsCon[current][0]]
                else:
                    message = "The constant value " + Reglas.constsCon[current][0] + "has never been declared"
                    raise SemanticException(message, Reglas.constsCon[current][1])

    def p_constantes_constid(p):
        'constantes : CONST CONSTID EQUAL CONSTID SEMICOLON constantes'

        toDefine = p[4]
        con = p[2]
        heredated = Reglas.consts.keys()
        if(con in heredated):
            message = "Constant " + con + " has already been declared"
            raise SemanticException(message, p.lineno(2))
        Reglas.constsCon[con] = [toDefine, p.lineno(2)]
        prev = p[-1][0]
        if prev == "encabezado":
            for current in Reglas.constsCon.keys():
                if Reglas.constsCon[current][0] in Reglas.consts.keys():
                    Reglas.consts[current] = Reglas.consts[Reglas.constsCon[current][0]]
                else:
                    message = "The constant value " + Reglas.constsCon[current][0] + "has never been declared"
                    raise SemanticException(message, Reglas.constsCon[current][1])

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
        mus = p[3]
        if not mus:
            message = "Voices defined must have at least one compas"
            raise SemanticException(message, p.lineno(3))
        p[0] = [p[1], mus]

    def p_decla_instrumento(p):
        'decla_instrumento : VOICE LPAREN NUMBER RPAREN'
        Reglas.cantvoices = Reglas.cantvoices + 1

        if(Reglas.cantvoices > 16):
            raise SemanticException("No se pueden configurar mas de 16 voces para el estandar", p.lineno(1))

        idInstrumento = p[3]
        if not(Reglas.instrumentoEnRango(idInstrumento)):
            msg = "El instrumento '" + str(idInstrumento) + "' no esta en el rango valido soportado por MIDI (0 a 127)"
            raise SemanticException(msg, p.lineno(3))

        p[0] = idInstrumento

    def p_decla_instrumento_const(p):
        'decla_instrumento : VOICE LPAREN CONSTID RPAREN'
        if(not(p[3] in Reglas.consts)):
        	message = "Constante " + p[3] + " no declarada!"
                raise SemanticException(message, p.lineno(3))
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
        if(duracion_compas != Reglas.dicc["compas_val"]):
            message = "El tiempo del compas es erroneo"
            raise SemanticException(message, p.lineno(1))
        else:
            p[0] = lista

    def p_bucle(p):
        'bucle : REPEAT LPAREN NUMBER RPAREN LCURL musica RCURL'
        p[0] = [p[3], p[6]]

    def p_bucle_constid(p):
        'bucle : REPEAT LPAREN CONSTID RPAREN LCURL musica RCURL'
        con = p[3]
        if(con in Reglas.consts.keys()):
            p[0] = [Reglas.consts[con], p[6]]
        else:
            message = "La constante " + con + " no esta definida"
            raise SemanticException(message, p.lineno(1))


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
        if not(Reglas.octavaEnRango(p[5])):
            raise SemanticException("El valor de octava definido como '"+ str(p[5])+"' esta fuera del rango permitido", p.lineno(5))

        p[0] = {}
        p[0]["duration"] = p[7]
        p[0]["nota"] = p[3][0]
        p[0]["desv"] = p[3][1]
        p[0]["octava"] = p[5]
        p[0]["type"] = "NOT"

# FALTA HACER QUE EN VEZ DE ACEPTAR UN NUMBER PUEDA ACEPTAR UN CONSTID
    def p_nota_prod_constid(p):
        'notaProd : NOTA LPAREN altura COMMA CONSTID COMMA duracion RPAREN SEMICOLON'
        var = p[5]
        if(not(var in Reglas.consts)):
            message = "Constante '" + var + "' no declarada"
            raise SemanticException(message, p.lineno(5))
        else:
            if not(Reglas.octavaEnRango(Reglas.consts[var])):
                raise SemanticException("El valor de octava definido como '"+ str(p[5])+"'=" + str(Reglas.consts[var]) +" esta fuera del rango permitido", p.lineno(5))

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
        Reglas.cantvoices = 1
        Reglas.dicc = {}
        Reglas.consts = {}
        Reglas.constsCon = {}
        message = "[Syntax error]"
        if token is not None:
            message += "\ntype:" + token.type
            message += "\nvalue:" + str(token.value)
            message += "\nline:" + str(token.lineno)
            message += "\nposition:" + str(token.lexpos) 
        
        raise Exception(message)

    yacc = yacc.yacc()
