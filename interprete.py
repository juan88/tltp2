
from yacc import yacc
import cmd

class Interprete(cmd.Cmd):
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = ">>"
		self.intro = "Bienvenido al interprete de Musileng"

	def default(self, line):
		result = yacc.parse(line)
		print result

if __name__ == '__main__':
	i = Interprete()
	i.cmdloop()
