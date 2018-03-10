from instructions import *

class Input:

	def __init__(self, instructions):
		self.instructions = instructions
		self.opcodes = []
		self.op = Opcode()

	def get_opcodes(self):
		self.opcodes = list(map(lambda x: self.op.get_opcode(x),self.instructions))

		return self.opcodes
