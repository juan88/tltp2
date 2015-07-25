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



	def calcularTempo(self, figura, duracion_negra):
	    	return 1000000 * 60 * figura / (4 * duracion_negra)


	def escribirEncabezado(self, ntracks, compas, tempo):
		res = """MFile 1 {ntracks} 384 
		MTrk
		000:00:000 TimeSig {compas} 24 8
		000:00:000 Tempo {tempo}
		000:00:000 Meta TrkEnd
		TrkEnd """
