import string
import math

class Traductor(object):
    
    figuras = {
      'redonda' : 1,
      'blanca' : 2,
      'negra' : 4,
      'corchea' : 8,
      'semicorchea' : 16,
      'fusa' : 32,
      'semifusa' : 64
    }


    notas = {
      'do' : 'c',
      're' : 'd',
      'mi' : 'e',
      'fa' : 'f',
      'sol' : 'g',
      'la' : 'a',
      'si' : 'b',
    }

    def __init__(self, timer):
        """ Inicializo un Traductor a partir de un CompasTimer que recibo como parametro"""
        self.timer = timer

    def valorParaFigura(self, nombre):
        """ Devuelvo el valor numerico de una figura musical """
        return Traductor.figuras[nombre]


    def calcularTempo(self, figura, figura_minuto):
        """ Calculo el tempo a partir de una figura y una duration por figura segun el formato midi """
        return 1000000 * 60 * self.valorParaFigura(figura) / (4 * figura_minuto)


    def escribirEncabezado(self, ntracks, compas, figura, figura_minuto):
        """ A partir de un string.Template escribo el encabezado del archivo a generar tomando los parametros
        que me pasan """
        tempo = self.calcularTempo(figura, figura_minuto)
        values = { 'ntracks':ntracks, 'compas':compas, 'tempo':str(tempo), 'tiempoInicial':self.timer.mostrar() }
        
        template =  """MFile 1 $ntracks 384 
MTrk
$tiempoInicial TimeSig $compas 24 8
$tiempoInicial Tempo $tempo
$tiempoInicial Meta TrkEnd
TrkEnd\n"""

        return string.Template(template).substitute(values)

    def escribirTrack(self, nroVoz, nroInstrumento, notas):
        """ Escribo un trakc para el nroDeVoz y de Instrumento que se pasa por parametro"""
        #todo: revisar que canal 10 solo para percusion
        values = {'tiempo': self.timer.mostrar(),
        'nroVoz':nroVoz,
        'nroInstrumento':nroInstrumento,
        'notas':self.escribirNotas(nroVoz, nroInstrumento, notas[nroInstrumento]),
        'tiempoFinal':self.timer.mostrar()
        }

        template = """MTrk
$tiempo Meta TrkName \"Voz $nroVoz\"
$tiempo ProgCh ch=$nroVoz prog=$nroInstrumento
$notas
$tiempoFinal Meta TrkEnd
TrkEnd
"""
        self.timer.reset()
        return string.Template(template).substitute(values)

    
    def escribirNotas(self, nroVoz, nroInstrumento, notas):
        ret = ''
        for nota in notas:
            if(nota['type'] == 'NOT'):
                ret += self.escribirNota(nroVoz, nroInstrumento, nota['nota'], nota['desv'], nota['octava'], nota['duration'])
            else:
                self.timer.avanzar(nota['duration'])
        return ret

    def escribirNota(self, nroVoz, nroInstrumento, nota, desv, octava, duration):
        """ A partir de un nro de instrumento escribo el valor de una nota para el documento a generar """
        valorNota = self.notaEnIngles(nota) + desv
        values = { 'tiempo':self.timer.mostrar(), 'canal':nroVoz, 'nota':valorNota+str(octava) }
        self.timer.avanzar(duration)
        values['tiempoLuego'] = self.timer.mostrar()

        template =  """$tiempo On ch=$canal note=$nota vol=70
$tiempoLuego Off ch=$canal note=$nota vol=0
"""
        return string.Template(template).substitute(values)

    def notaEnIngles(self, nota):
        """ Devuelve el valor de la nota segun el sistema anglosajon de notas musicales """
        return Traductor.notas[nota]

class CompasTimer(object):
    
    CLICKS_POR_PULSO = 384

    tiempos = {
        1.0 : 'redonda',
        0.5 : 'blanca',
        0.25 : 'negra',
        0.125 : 'corchea',
        0.0625 : 'semicorchea',
        0.03125 : 'fusa',
        0.015625 : 'semifusa'
    }

    def __init__(self, numerador, denominador):
        """ Constructor del timer para compas. Necesita numerador y denominador para
        poder calcular los valores de las notas segun cada compas"""
        self.numerador = numerador
        self.denominador = denominador
        self.compas = 0
        self.pulso = 0
        self.click = 0

    def clicksPorFigura(self, figura):
        """ Devuelvo la cantidad de clicks por figura de acuerdo a la configuracion del compas """
        traductor = Traductor(self)
        clicksPorRedonda = CompasTimer.CLICKS_POR_PULSO * self.denominador 
        return clicksPorRedonda / traductor.valorParaFigura(figura)

    def mostrar(self):
        """ Devuelvo una representacion de string del tiempo actual """
        compas = str(self.compas)
        pulso = str(self.pulso)
        click = str(self.click)
        return string.zfill(compas, 3) + ":" + string.zfill(pulso,2) + ":" + string.zfill(click,3)

    def avanzar(self, figura):
        """ Avanza el timer segun el valor de la figura en cuestion """
        clicksASumar = self.clicksPorFigura(self.tiempos[figura])
        pulsosASumar = int(math.floor(clicksASumar / CompasTimer.CLICKS_POR_PULSO))
        clicksFraccion = clicksASumar - pulsosASumar * CompasTimer.CLICKS_POR_PULSO
        compasesASumar = 0

        if(self.click + clicksFraccion >= CompasTimer.CLICKS_POR_PULSO):    
            pulsosASumar+=1
            self.click = CompasTimer.CLICKS_POR_PULSO - (clicksFraccion + self.click)
        else:
            self.click += clicksFraccion

        self.pulso += pulsosASumar
        if(self.pulso >= self.numerador):
            compasesASumar = int(math.floor(self.pulso / self.numerador))
            self.pulso = self.pulso % self.numerador
        
        self.compas += compasesASumar

    def reset(self):
    	self.compas = 0
    	self.pulso = 0
    	self.click = 0
