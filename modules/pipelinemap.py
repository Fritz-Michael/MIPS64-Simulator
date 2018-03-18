from internalregisters import *

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
		print(*self.cycles)
		print(self.internal_registers.registers.R)


if __name__ == '__main__':
	instructions = ['64010003']
	# a = hex(int(bin(int(instructions[0],16))[2:].zfill(32)[6:11],2))[2:].zfill(16).upper()
	# print(int(a,16))
	temp = Pipeline(instructions)
	temp.get_pipeline()