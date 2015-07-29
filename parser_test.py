# -*- coding: utf-8 -*-
#!/usr/bin/python

import unittest
import lexer_rules
import parser_rules
import os
from traductor import *

from sys import argv, exit
from ply.lex import lex
from ply.yacc import yacc


class ParserTest(unittest.TestCase):
    
    # def testTraductor1(self):
    #     expresion = """#tempo redonda 60
    #     #compas 2/2
    #     """
    #     ast = self.parser(expresion)
    #     self.assertTrue(isinstance(ast, Traductor))

    # def testTraductor2(self):
    #     expresion = self.leer_archivo("entradas_de_prueba/encabezado1.mus")
    #     ast = self.parser(expresion)
    #     self.assertTrue(isinstance(ast, Traductor))


    def testTraductor1(self):
        expresion = self.leer_archivo("entradas_de_prueba/entrada_ok_1.mus")
        ast = self.parser(expresion)

    def testTraductor2(self):
        expresion = self.leer_archivo("entradas_de_prueba/entrada_ok_4.mus")
        ast = self.parser(expresion)

    def testTraductor3(self):
        expresion = self.leer_archivo("entradas_de_prueba/entrada_ok_2.mus")
        ast = self.parser(expresion)

    def testTraductor4(self):
        expresion = self.leer_archivo("entradas_de_prueba/entrada_ok_3.mus")
        ast = self.parser(expresion)

    def testTraductor5(self):
        expresion = self.leer_archivo("entradas_de_prueba/parsingtest_wrongtimecompas.mus")
        with self.assertRaises(Exception):
            ast = self.parser(expresion)

    def testTraductor6(self):
        expresion = self.leer_archivo("entradas_de_prueba/entrada_error_def_compas_malformada.mus")
        with self.assertRaises(Exception):
            ast = self.parser(expresion)

    def testTraductor7(self):
        expresion = self.leer_archivo("entradas_de_prueba/entrada_error_longitud_mal_formada_de_compas.mus")
        with self.assertRaises(Exception):
            ast = self.parser(expresion)

    def testTraductor8(self):
        expresion = self.leer_archivo("entradas_de_prueba/entrada_def_tempo_malformada.mus")
        with self.assertRaises(Exception):
            ast = self.parser(expresion)

    def testTraductor9(self):
        expresion = self.leer_archivo("entradas_de_prueba/entrada_errores_varios")
        with self.assertRaises(Exception):
            ast = self.parser(expresion)

    def testTraductor10(self):
        expresion = self.leer_archivo("entradas_de_prueba/entrada_error_bloque_no_cerrado.mus")
        with self.assertRaises(Exception):
            ast = self.parser(expresion)

    # Funciones utilitarias
    def parser(self, expresion):
        variables = parser_rules.Reglas()
        lexer = lex(module=lexer_rules)
        parser = parser_rules.yacc
        # parser = yacc(module=parser_rules)
        return parser.parse(expresion, lexer)

    def leer_archivo(self, ruta):
        if not os.path.exists(ruta):
            sys.exit("El archivo '%s' no existe." % ruta)
        elif not os.path.isfile(ruta):
            sys.exit("El archivo '%s' es invalido." % ruta)

        archivo = open(ruta, "r")
        return archivo.read()



def main():
    unittest.main()

if __name__ == '__main__':
    main()