# -*- coding: utf-8 -*-
#!/usr/bin/python

import unittest
import lexer_rules
import os

from sys import argv, exit
from ply.lex import lex
from ply.yacc import yacc


class LexerTest(unittest.TestCase):

    def testLeoEncabezadoYValidoTokens1(self):
        expresion = self.leer_archivo("entradas_de_prueba/encabezado1.mus")
        lexer = self.lexer(expresion)
        token = lexer.token()
        # print "test1"
        # print token
        while token is not None:
            # print "test1"
            # print token.value
            token = lexer.token()

        self.assertTrue(True)

    def testLeoEncabezadoYValidoTokens2(self):
        expresion = self.leer_archivo("entradas_de_prueba/encabezado2.mus")
        lexer = self.lexer(expresion)
        
        token = lexer.token()
        while token is not None:
            # print "test2"
            # print token.type
            # print token.value
            token = lexer.token()

        self.assertTrue(True)


    def testTokensLinea1(self):
        lexer = self.lexer("#tempo redonda 60")
        esperados = ['HASH', 'TEMPO', 'FIGURE', 'NUMBER']
        #print "test3"
        #for lex in lexer:
        #    print lex
        self.assertTokens(esperados, lexer)

    def testTokensLinea2(self):
        lexer = self.lexer("#compas 2/2")
        esperados = ['HASH', 'COMPAS', 'NUMBER', 'DIV', 'NUMBER']
        self.assertTokens(esperados, lexer)

    def testTokensLinea3(self):
        lexer = self.lexer("const octava = 5;")
        esperados = ['CONST', 'CONSTID', 'EQUAL', 'NUMBER', 'SEMICOLON']
        self.assertTokens(esperados, lexer)

    def testTokensLinea3ConComenarios(self):
        lexer = self.lexer("const octava = 5; //Esto es un comentario")
        esperados = ['CONST', 'CONSTID', 'EQUAL', 'NUMBER', 'SEMICOLON']
        self.assertTokens(esperados, lexer)

    def testTokensLinea3ConComenarios2(self):
        lexer = self.lexer("""//Otro comentario
            const octava = 5; //Esto es un comentario""")
        esperados = ['CONST', 'CONSTID', 'EQUAL', 'NUMBER', 'SEMICOLON']
        self.assertTokens(esperados, lexer)

    def testNotaId(self):
        lexer = self.lexer("nota(do, 2, blanca);")
        esperados2 = ['NOTA', 'LPAREN', 'NOTAID', 'COLON', 'NUMBER', 'COLON', 'FIGURE', 'RPAREN', 'SEMICOLON']
        self.assertTokens(esperados2, lexer)

    def assertTokens(self, esperados, lexer2):
        """ Assert una lista de tokens supuestamente consumidos ok por el lexer pasado como parametro """
        obtenidos = []
        token = lexer2.token()
        while token is not None:
            obtenidos.append(token.type)
            token = lexer2.token()

        for index, val in enumerate(esperados):
            self.assertEqual(obtenidos[index], esperados[index])


    def lexer(self, expresion):
        lexer = lex(module=lexer_rules)
        lexer.input(expresion)
        return lexer

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