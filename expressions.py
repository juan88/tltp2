class Expresion(object):

	def evaluar(self):
		# Aca se implementa cada tipo de expresion.
		raise NotImplementedError


class Encabezado(Expression):
	pass

class Traductor(Expression):
	pass
