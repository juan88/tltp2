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
