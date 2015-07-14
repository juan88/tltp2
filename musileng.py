import lexer_rules
import parser_rules
import os

from sys import argv, exit

from ply.lex import lex
from ply.yacc import yacc


if __name__ == "__main__":
    if len(argv) != 3:
        print "Invalid arguments."
        print "Use:"
        print "  musileng.py entrada.mus salida.txt"
        exit()

    parametros = sys.argv[1:]

    entrada = archivo_para_leer(parametros[0])
    salida = archivo_para_escribir(parametros[1])

    lexer = lex(module=lexer_rules)
    parser = yacc(module=parser_rules)

    expression = parser.parse(text, lexer)

    result = expression.evaluate()
    print result
    entrada.close()
    salida.close()


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