import lexer_rules
import parser_rules
from traductor import *
import os

from sys import argv, exit

from ply.lex import lex
from ply.yacc import yacc



def archivo_para_leer(ruta):
    if not os.path.exists(ruta):
        sys.exit("El archivo '%s' no existe." % ruta)
    elif not os.path.isfile(ruta):
        sys.exit("El archivo '%s' es invalido." % ruta)

    return open(ruta, "r")


def archivo_para_escribir(ruta):
    ruta_completa = os.path.realpath(ruta)
    directorio = os.path.dirname(ruta_completa)
    if not os.access(directorio, os.W_OK):
        sys.exit("El archivo '%s' no puede escribirse." % ruta)

    return open(ruta, "w")


# def parser(expresion):

#     lexer = lex(module=lexer_rules)
#     parser = parser_rules.yacc
#     # parser = yacc(module=parser_rules)
#     return parser.parse(expresion, lexer)

if __name__ == "__main__":
    if len(argv) != 3:
        print "Invalid arguments."
        print "Use:"
        print "  musileng.py entrada.mus salida.txt"
        exit()

    parametros = argv[1:]

    entrada = archivo_para_leer(parametros[0])
    salida = archivo_para_escribir(parametros[1])

    text = entrada.read()
    print text
    variables = parser_rules.Reglas()
    lexer = lex(module=lexer_rules)
    parser = parser_rules.yacc

    expression = parser.parse(text, lexer)
    encabezado = expression[0]
    print "encabezado: "
    print encabezado
    voces = expression[1]
    print "voces: "
    print voces

    numeradorCompas = encabezado[1][0]
    denomCompas = encabezado[1][1]

    traductor = Traductor(CompasTimer(numeradorCompas,denomCompas))

    ntracks = len(voces) + 1
    compas = str(numeradorCompas) + "/" + str(denomCompas)
    figura = encabezado[0][0]
    print figura
    tempofigura = encabezado[0][1]
    print tempofigura
    escribirEncabezado = traductor.escribirEncabezado(ntracks, compas, figura, tempofigura)
    print escribirEncabezado

    entrada.close()
    salida.close()

