# -*- coding: utf-8 -*-
#!/usr/bin/python

import unittest
import lexer_rules
import os

from sys import argv, exit
from ply.lex import lex
from ply.yacc import yacc


class LexerTest(unittest.TestCase):

    def testTokensLinea1(self):
        lexer = self.lexer("#tempo redonda 60")
        esperados = ['HASH', 'TEMPO', 'FIGURE', 'NUMBER']
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
        esperados2 = ['NOTA', 'LPAREN', 'NOTAID', 'COMMA', 'NUMBER', 'COMMA', 'FIGURE', 'RPAREN', 'SEMICOLON']
        self.assertTokens(esperados2, lexer)

    def testSilencio(self):
        lexer = self.lexer("silencio(blanca);")
        esperados2 = ['SILENCIO', 'LPAREN', 'FIGURE', 'RPAREN', 'SEMICOLON']
        self.assertTokens(esperados2, lexer)    
    
    def testCompas(self):
        """ Testeo un compas entero para ver tome bien los tokens definidos"""
        texto = """compas
        {
            nota(si, octava, blanca);
            // esto es un silencio que dura una blanca.
            silencio(blanca);
        }"""
        
        lexer = self.lexer(texto)
        esperados2 = ['COMPAS', 'LCURL', 'NOTA', 'LPAREN', 'NOTAID', 'COMMA', 'CONSTID', 'COMMA', 'FIGURE', 'RPAREN', 'SEMICOLON',
            'SILENCIO', 'LPAREN', 'FIGURE', 'RPAREN', 'SEMICOLON', 'RCURL']
        self.assertTokens(esperados2, lexer)

    def testRepetir1(self):
        """ Testeo un bloque repetir para ver tome bien los tokens definidos"""
        texto = """repetir(10) {
            compas
            {
                nota(si, octava, blanca);
                nota(do, octava, blanca);
            }
        }"""
        
        lexer = self.lexer(texto)
        esperados2 = [
            'REPEAT', 'LPAREN', 'NUMBER', 'RPAREN', 'LCURL',
                'COMPAS', 'LCURL', 
                    'NOTA', 'LPAREN', 'NOTAID', 'COMMA', 'CONSTID', 'COMMA', 'FIGURE', 'RPAREN', 'SEMICOLON',
                    'NOTA', 'LPAREN', 'NOTAID', 'COMMA', 'CONSTID', 'COMMA', 'FIGURE', 'RPAREN', 'SEMICOLON',
                'RCURL',
            'RCURL']
        self.assertTokens(esperados2, lexer)

    def testRepetir2(self):
        """ Testeo un bloque repetir un poco más complejo para ver tome bien los tokens definidos"""
        texto = """repetir(3) {
            compas
            {
                nota(si, octava, blanca);
                nota(do, octava, blanca);
            }
            compas
            {
                nota(do, octava, semifusa);
            }
        }"""
        
        lexer = self.lexer(texto)
        esperados2 = [
            'REPEAT', 'LPAREN', 'NUMBER', 'RPAREN', 'LCURL',
                'COMPAS', 'LCURL', 
                    'NOTA', 'LPAREN', 'NOTAID', 'COMMA', 'CONSTID', 'COMMA', 'FIGURE', 'RPAREN', 'SEMICOLON',
                    'NOTA', 'LPAREN', 'NOTAID', 'COMMA', 'CONSTID', 'COMMA', 'FIGURE', 'RPAREN', 'SEMICOLON',
                'RCURL',
                'COMPAS', 'LCURL', 
                    'NOTA', 'LPAREN', 'NOTAID', 'COMMA', 'CONSTID', 'COMMA', 'FIGURE', 'RPAREN', 'SEMICOLON',
                'RCURL',
            'RCURL']
        self.assertTokens(esperados2, lexer)    

    def testVoz(self):
        """ Testeo un de voz"""
        texto = """voz(esto_es_una_constante) {
            compas
            {
                nota(si, octava, blanca);
                nota(do, octava, blanca);
            }
        }"""
        
        lexer = self.lexer(texto)
        esperados2 = [
            'VOICE', 'LPAREN', 'CONSTID', 'RPAREN', 'LCURL',
                'COMPAS', 'LCURL', 
                    'NOTA', 'LPAREN', 'NOTAID', 'COMMA', 'CONSTID', 'COMMA', 'FIGURE', 'RPAREN', 'SEMICOLON',
                    'NOTA', 'LPAREN', 'NOTAID', 'COMMA', 'CONSTID', 'COMMA', 'FIGURE', 'RPAREN', 'SEMICOLON',
                'RCURL',
            'RCURL']
        self.assertTokens(esperados2, lexer)


    def testKeywordsYPrefijos(self):
        texto = """ const piano = 0;
const constante = 6;
const compasito = 3;
const tempoo = 2;
const silencioporfavor = 1;
const aaasilencio = 1;
const voza = 2;
const redondaYDeRicota = 1;
const mifasollasidoremihola = 1;
const repetirr = 6; """
        lexer = self.lexer(texto)
        esperados = ['CONST', 'CONSTID', 'EQUAL', 'NUMBER', 'SEMICOLON',
        'CONST', 'CONSTID', 'EQUAL', 'NUMBER', 'SEMICOLON',
        'CONST', 'CONSTID', 'EQUAL', 'NUMBER', 'SEMICOLON',
        'CONST', 'CONSTID', 'EQUAL', 'NUMBER', 'SEMICOLON',
        'CONST', 'CONSTID', 'EQUAL', 'NUMBER', 'SEMICOLON',
        'CONST', 'CONSTID', 'EQUAL', 'NUMBER', 'SEMICOLON',
        'CONST', 'CONSTID', 'EQUAL', 'NUMBER', 'SEMICOLON',
        'CONST', 'CONSTID', 'EQUAL', 'NUMBER', 'SEMICOLON',
        'CONST', 'CONSTID', 'EQUAL', 'NUMBER', 'SEMICOLON',
        'CONST', 'CONSTID', 'EQUAL', 'NUMBER', 'SEMICOLON']
        self.assertTokens(esperados, lexer)


    # Funciones utilitarias
    def assertTokens(self, esperados, lexer2):
        """ Assert una lista de tokens supuestamente consumidos ok por el lexer pasado como parametro """
        obtenidos = []
        token = lexer2.token()
        while token is not None:
            #print token #descomentar para debugging. Muy útil!
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