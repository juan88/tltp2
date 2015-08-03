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

        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_bucles_anidados_puntillos.mus')
        salida = musileng.archivo_para_escribir('salidas/salidaBuclesPuntillos.mus')
        musileng.convertir(entrada, salida)

        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_ok_constante_foo1_1.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_constante_foo1_1.mus')
        musileng.convertir(entrada, salida)

        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_ok_repetir_constante.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_repetir_constante.mus')
        musileng.convertir(entrada, salida)

        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_ok_constante_definida.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_constante_definida.mus')
        musileng.convertir(entrada, salida)


        self.assertTrue(os.path.isfile('salidas/salida1.mus'))
        self.assertTrue(os.path.isfile('salidas/salida2.mus'))
        self.assertTrue(os.path.isfile('salidas/salida3.mus'))
        self.assertTrue(os.path.isfile('salidas/salida4.mus'))
        self.assertTrue(os.path.isfile('salidas/salida5.mus'))
        self.assertTrue(os.path.isfile('salidas/salida_constante_foo1_1.mus'))
        self.assertTrue(os.path.isfile('salidas/salida_repetir_constante.mus'))
        self.assertTrue(os.path.isfile('salidas/salida_constante_definida.mus'))

    def testDefinicionTempoMalformada(self):
        """ Definicion de tempo malformada """
        musileng = Musileng()
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_def_tempo_malformada.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        with self.assertRaises(Exception):
		musileng.convertir(entrada, salida)

    def testBloqueNoCerrado(self):
        """ Definicion de tempo malformada """
        musileng = Musileng()
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_bloque_no_cerrado.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        with self.assertRaises(Exception):
                musileng.convertir(entrada, salida)

    def testCompasVacio(self):
        """ Compas vacio """
        musileng = Musileng()
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_compas_vacio.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        with self.assertRaises(Exception):
                musileng.convertir(entrada, salida)

    def testDefinicionDeCompasMalformada(self):
        """ Definicion de compas malformada """
        musileng = Musileng()            
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_def_compas_malformada.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        with self.assertRaises(Exception):
                musileng.convertir(entrada, salida)

    def testEntradaErroresVarios(self):
        """ Entrada con varios errores """
        musileng = Musileng()
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_errores_varios')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        with self.assertRaises(Exception):
                musileng.convertir(entrada, salida)
    
    def testLongitudMalformadaDeCompas(self):
        """ Mal configurada la longitud del compas """
        musileng = Musileng()
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_longitud_mal_formada_de_compas.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        with self.assertRaises(Exception):
                musileng.convertir(entrada, salida)

    def testErrorConConstanteRepetida(self):
        """ Error cuando se tiene una constante repetida """
        musileng = Musileng()
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_constante_repetida.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        with self.assertRaises(Exception):
                musileng.convertir(entrada, salida)

    def testErrorTempoMayorACero(self): #Ojo que falla pero por división por cero. Debería fallar por lo que verdaderamente corresponde.
        """ El tempo debe ser mayor a 0 """
        musileng = Musileng()
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_tempo_blanca_0.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        with self.assertRaises(Exception):
                musileng.convertir(entrada, salida)

    def testErrorAlMenosUnaVozDefinida(self):
        """ Debe haber al menos una voz definida """
        musileng = Musileng()
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_voz_no_definida.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        with self.assertRaises(Exception):
                musileng.convertir(entrada, salida)


    def testErrorOctavaFueraDeRango(self):
        """ Se define una octava fuera de rango """
        musileng = Musileng()
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_octava_fuera_rango.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        with self.assertRaises(Exception):
                musileng.convertir(entrada, salida)

        musileng = Musileng()
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_octava_fuera_rango2.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        with self.assertRaises(Exception):
                musileng.convertir(entrada, salida)



    def testErrorConMasDe16Voces(self):
        """ No puede haber mas de 16 voces """
        musileng = Musileng()
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_voz_17_veces.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        with self.assertRaises(Exception):
                musileng.convertir(entrada, salida)

    def testVozFueraDeRango(self):
        """ No se puede configurar un valor de instrumento por fuera del rango permitido """
        musileng = Musileng()
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_voz_fuera_rango.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        with self.assertRaises(Exception):
                musileng.convertir(entrada, salida)

    def testVozVacia(self):
        """ No se puede configurar una voz vacía """
        musileng = Musileng()
        entrada = musileng.archivo_para_leer('entradas_de_prueba/entrada_error_voz_vacia.mus')
        salida = musileng.archivo_para_escribir('salidas/salida_error.mus')
        with self.assertRaises(Exception):
                musileng.convertir(entrada, salida)
            

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
