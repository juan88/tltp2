# -*- coding: utf-8 -*-
#!/usr/bin/python
import unittest
import os
from musileng import *
from sys import argv, exit

class MusilengTest(unittest.TestCase):
    
    
    def testArchivosOk(self):
        """ Testeo que musileng lea y escriba los archivos que estan ok """
        musileng = Musileng()
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_ok_1.mus')
        salida = musileng.archivo_para_escribir('salidas/salida1.mus')
        musileng.convertir(entrada, salida)
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_ok_2.mus')
        salida = musileng.archivo_para_escribir('salidas/salida2.mus')
        musileng.convertir(entrada, salida)
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_ok_3.mus')
        salida = musileng.archivo_para_escribir('salidas/salida3.mus')
        musileng.convertir(entrada, salida)
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_ok_4.mus')
        salida = musileng.archivo_para_escribir('salidas/salida4.mus')
        musileng.convertir(entrada, salida)
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_ok_5.mus')
        salida = musileng.archivo_para_escribir('salidas/salida5.mus')
        musileng.convertir(entrada, salida)

        self.assertTrue(os.path.isfile('salidas/salida1.mus'))
        self.assertTrue(os.path.isfile('salidas/salida2.mus'))
        self.assertTrue(os.path.isfile('salidas/salida3.mus'))
        self.assertTrue(os.path.isfile('salidas/salida4.mus'))
        self.assertTrue(os.path.isfile('salidas/salida5.mus'))

    def testArchivosNoOk(self):
        """ Testeo que musileng tire excepciones para los archivos que no estan ok """
        musileng = Musileng()
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_def_tempo_malformada.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        self.assertRaises(Exception, musileng.convertir, entrada, salida)

        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_bloque_no_cerrado.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        self.assertRaises(Exception, musileng.convertir, entrada, salida)

        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_compas_vacio.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        self.assertRaises(Exception, musileng.convertir, entrada, salida)

        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_constante_definida_dos_veces.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        self.assertRaises(Exception, musileng.convertir, entrada, salida)

        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_def_compas_malformada.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        self.assertRaises(Exception, musileng.convertir, entrada, salida)

        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_errores_varios.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        self.assertRaises(Exception, musileng.convertir, entrada, salida)
        

        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_longitud_mal_formada_de_compas.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        self.assertRaises(Exception, musileng.convertir, entrada, salida)
        
        
        


    # Funciones utilitarias
    def leerArchivo(self, ruta):
        if not os.path.exists(ruta):
            sys.exit("El archivo '%s' no existe." % ruta)
        elif not os.path.isfile(ruta):
            sys.exit("El archivo '%s' es invalido." % ruta)

        archivo = open(ruta, "r")
        return archivo.read()

    def escribirOutput(self, texto, ruta):
        """ Escribe un archivo con el output generado """
        ruta_completa = os.path.realpath(ruta)
        directorio = os.path.dirname(ruta_completa)
        out = open(ruta, "w")
        out.write(texto)
        out.close()

def main():
    unittest.main()

if __name__ == '__main__':
    main()