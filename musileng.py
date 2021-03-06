import lexer_rules
import parser_rules
from traductor import *
import os

from sys import argv, exit
import sys

from ply.lex import lex
from ply.yacc import yacc

class Musileng(object):

    def archivo_para_leer(self, ruta):
        if not os.path.exists(ruta):
            sys.exit("El archivo '%s' no existe." % ruta)
        elif not os.path.isfile(ruta):
            sys.exit("El archivo '%s' es invalido." % ruta)

        return open(ruta, "r")


    def archivo_para_escribir(self, ruta):
        ruta_completa = os.path.realpath(ruta)
        directorio = os.path.dirname(ruta_completa)
        if not os.access(directorio, os.W_OK):
            sys.exit("El archivo '%s' no puede escribirse." % ruta)

        return open(ruta, "w")


    def convertir(self, entrada, salida):

        entradaFile = self.archivo_para_leer(entrada)
        text = entradaFile.read()

        #Inicializo variables
        variables = parser_rules.Reglas()
        
        lexer = lex(module=lexer_rules)
        parser = parser_rules.yacc

        expression = parser.parse(text, lexer)
        encabezado = expression[0]
        voces = expression[1]

        numeradorCompas = encabezado[1][0]
        denomCompas = encabezado[1][1]

        traductor = Traductor(CompasTimer(numeradorCompas,denomCompas))

        ntracks = len(voces) + 1
        compas = str(numeradorCompas) + "/" + str(denomCompas)
        figura = encabezado[0][0]
        tempofigura = encabezado[0][1]
        escribirEncabezado = traductor.escribirEncabezado(ntracks, compas, figura, tempofigura)

        voices = {}
        track = 1
        salidaStr = escribirEncabezado
        for voz in voces:
            instrumento = voz[0]
            notas = []

            #ELIMINAMOS LOS BUCLES Y NOS QUEDAMOS CON LISTA DE COMPASES EXCLUSIVAMENTE
            original = voz[1]
            aRecorrer = original
            hayCambios = True
            while hayCambios:
                hayCambios = False
                original = aRecorrer
                aRecorrer = []
                for compas in original:
                    if(compas[0] == 'C'):
                        aRecorrer = aRecorrer + [compas]
                    else:
                        compasesBucle = compas[1][1]
                        for i in range(compas[1][0]):
                            for compas in compasesBucle:
                                aRecorrer = aRecorrer + [compas]
                        hayCambios = True
            for compas in aRecorrer:
                for nota in compas[1]:
                    notas = notas + [nota]
            voices[instrumento] = notas
            escribirTrack = traductor.escribirTrack(track, instrumento, voices)
            salidaStr = salidaStr + escribirTrack
            track = track + 1
            if(track == 10):
                track = 11

        salidaFile = self.archivo_para_escribir(salida)
        salidaFile.write(salidaStr)

        entradaFile.close()
        salidaFile.close()


    def restart(self):
        parser_rules.Reglas().restart()

#Main para correr el programa
if __name__ == "__main__":
    if len(argv) != 3:
        print "Invalid arguments."
        print "Use:"
        print "  musileng.py entrada.mus salida.txt"
        exit()

    parametros = argv[1:]

    musileng = Musileng()
    entrada = parametros[0]
    salida = parametros[1]

    try:
        musileng.convertir(entrada, salida)
    except parser_rules.SemanticException as e:
        e.filename = entrada
        print " Musileng > ERROR Semantico!!"
        print e.errorMsg()

