from internalregisters import *
from instructions import *

class Pipeline:

	def __init__(self, instructions):
		self.instructions = instructions
		self.internal_registers = InternalRegisters(instructions)
		self.cycles = []

	def get_pipeline(self):
		end = False

		while not end:
			cycle = [None,None,None,None,None]

			if self.internal_registers.writeback():
				cycle[4] = 'WB'
				if self.internal_registers.wb.IR == self.instructions[-1]:
					end = True
			if self.internal_registers.memory_access():
				cycle[3] = 'MEM'
			if self.internal_registers.execution():
				cycle[2] = 'EX'
			if self.internal_registers.instruction_decode():
				cycle[1] = 'ID'
			if self.internal_registers.instruction_fetch():
				cycle[0] = 'IF'
			self.cycles.append(cycle)
		print(self.cycles)


if __name__ == '__main__':
	instructions = ['BC L1','DADDIU R2, R0, #0003','L1: DADDU R3, R1, R2']
	opcode = Opcode(instructions)
	ins = list(map(lambda x: opcode.get_opcode(x),instructions))
	print(ins)
	temp = Pipeline(ins)
	temp.get_pipeline()
	print(temp.internal_registers.registers.R)