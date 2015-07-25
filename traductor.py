class Expresion(object):

    def evaluar(self):
        # Aca se implementa cada tipo de expresion.
        raise NotImplementedError


class Encabezado(Expresion):
    
    def __init__(self, tempo, compas):
        self.tempo = tempo
        self.compas = compas

class Traductor(Expresion):
    
    def __init__(self, encabezado, constantes, voces):
        self.encabezado = encabezado
        self.constantes = constantes
        self.voces = voces

    def calcularTempo(self, figura, figuras_minuto):
        return 1000000 * 60 * figura / (4 * figuras_minuto)


    def escribirEncabezado(self, ntracks, compas, tempo):
        return """MFile 1 {ntracks} 384 
        MTrk
        000:00:000 TimeSig {compas} 24 8
        000:00:000 Tempo {self.calcularTempo(tempo)}
        000:00:000 Meta TrkEnd
        TrkEnd"""

    def escribirTrack(self, nroVoz, nroInstrumento):
        #todo: revisar que canal 10 solo para percusión !!
        ret = "MTrk"
        ret += "000:00:000 Meta TrkName \"Voz {nroVoz}\""
        ret += "000:00:000 ProgCh ch={nroVoz} prog={nroInstrumento}"
        ret += self.escribirNotas(nroInstrumento, nroVoz)
        ret += "TrkEnd"
        return ret

    def clicksPorFigura(self, figura, denominador):
        clicksPorPulso = 384
        clicksPorRedonda = clicksPorPulso * denominador 
        return clicksPorRedonda / figura

    def escribirNotas(self, nroInstrumento):
        for notas in instrumento[nroInstrumento]:

