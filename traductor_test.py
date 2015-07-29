# -*- coding: utf-8 -*-
#!/usr/bin/python
import unittest
import os
from traductor import *
from sys import argv, exit

class TraductorTest(unittest.TestCase):
    
    def testNombreFigura(self):
        """Testeo que una figura (string) me devuelva el valor que tiene esta asociado"""
        traductor = Traductor(CompasTimer(3,4))
        self.assertEquals(traductor.valorParaFigura('redonda'),1)
        self.assertEquals(traductor.valorParaFigura('blanca'),2)
        self.assertEquals(traductor.valorParaFigura('negra'),4)

    def testTempo(self):
        """ Testeo que el tempo sea correctamente calculado para el valor de figura y tiempo por figura"""
        traductor = Traductor(CompasTimer(3,4))
        self.assertEquals(traductor.calcularTempo('redonda',60), 250000)

    def testEscribirEncabezado(self):
        """ Escribo un encabezado correcto para los datos administrados """
        traductor = Traductor(CompasTimer(3,4))
        testigo = """MFile 1 2 384 
        MTrk
        000:00:000 TimeSig 2/2 24 8
        000:00:000 Tempo 250000
        000:00:000 Meta TrkEnd
        TrkEnd"""

        self.assertEquals(testigo, traductor.escribirEncabezado(2, '2/2', 'redonda', 60))

    def testClicksPorFigura(self):
        """ Testeo el calculo de clicks por figura """
        timer = CompasTimer(3,4)
        self.assertEquals(384, timer.clicksPorFigura('negra'))
        self.assertEquals(384*2, timer.clicksPorFigura('blanca'))
        self.assertEquals(384*4, timer.clicksPorFigura('redonda'))

        timer = CompasTimer(3,8)
        self.assertEquals(384*2, timer.clicksPorFigura('negra'))
        self.assertEquals(384, timer.clicksPorFigura('corchea'))
        self.assertEquals(192, timer.clicksPorFigura('semicorchea'))

    def testChequearComoSeMuestraElTimestampDeNotas(self):
        timer = CompasTimer(3,4)
        self.assertEquals('000:00:000', timer.mostrar())
        timer.compas = 1
        timer.pulso = 1
        timer.click = 192
        self.assertEquals('001:01:192', timer.mostrar())


    def testAritmeticaDeClicks1(self):
        timer = CompasTimer(2,4)
        self.assertEquals('000:00:000', timer.mostrar())
        timer.avanzar('negra')
        self.assertEquals('000:01:000', timer.mostrar())
        timer.avanzar('corchea')
        self.assertEquals('000:01:192', timer.mostrar())
        timer.avanzar('corchea')
        self.assertEquals('001:00:000', timer.mostrar())
        timer.avanzar('blanca')
        self.assertEquals('002:00:000', timer.mostrar())
        timer.avanzar('redonda')
        self.assertEquals('004:00:000', timer.mostrar())

    def testAritmeticaDeClicks2(self):
        timer = CompasTimer(2,4)
        self.assertEquals('000:00:000', timer.mostrar())
        timer.avanzar('negra')
        self.assertEquals('000:01:000', timer.mostrar())
        timer.avanzar('corchea')
        self.assertEquals('000:01:192', timer.mostrar())
        timer.avanzar('corchea')
        self.assertEquals('001:00:000', timer.mostrar())
        timer.avanzar('corchea')
        self.assertEquals('001:00:192', timer.mostrar())
        timer.avanzar('blanca')
        self.assertEquals('002:00:192', timer.mostrar())
        timer.avanzar('redonda')
        self.assertEquals('004:00:192', timer.mostrar())

    def testValorNotaEnIngles(self):
        traductor = Traductor(CompasTimer(3,4))
        self.assertEquals('a', traductor.notaEnIngles('la'))
        self.assertEquals('c', traductor.notaEnIngles('do'))
        self.assertEquals('d', traductor.notaEnIngles('re'))

    def testEscriboDosaNotas(self):
        traductor = Traductor(CompasTimer(2,4))
        notas = [{'nota':'do', 'octava':5, 'duracion':'corchea'}, {'nota':'re', 'octava':5, 'duracion':'corchea'}]
        testigo = """000:00:000 On ch=1 note=c5 vol=70
000:00:192 Off ch=1 note=c5 vol=0
000:00:192 On ch=1 note=d5 vol=70
000:01:000 Off ch=1 note=d5 vol=0
"""
        self.assertEquals(testigo, traductor.escribirNotas(1, notas))

    def testTrack1(self):
        traductor = Traductor(CompasTimer(2,4))
        nroInstrumento = 1
        notas = { nroInstrumento : [{'nota':'do', 'octava':5, 'duracion':'corchea'}, {'nota':'re', 'octava':5, 'duracion':'corchea'}] }
        testigo = """MTrk
000:00:000 Meta TrkName "Voz 1"
000:00:000 ProgCh ch=1 prog=1
000:00:000 On ch=1 note=c5 vol=70
000:00:192 Off ch=1 note=c5 vol=0
000:00:192 On ch=1 note=d5 vol=70
000:01:000 Off ch=1 note=d5 vol=0

000:01:000 Meta TrkEnd
TrkEnd
"""
        self.assertEquals(testigo, traductor.escribirTrack(1, 1, notas))

    def testReseteoTimer(self):
        timer = CompasTimer(2,4)
        self.assertEquals('000:00:000', timer.mostrar())
        timer.avanzar('negra')
        timer.avanzar('corchea')
        timer.avanzar('corchea')
        timer.avanzar('corchea')
        timer.avanzar('blanca')
        timer.avanzar('redonda')
        self.assertEquals('004:00:192', timer.mostrar())
        timer.reset()
        self.assertEquals('000:00:000', timer.mostrar())

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