from internalregisters import *

class Pipeline:

	def __init__(self, instructions):
		self.instructions = instructions
		self.internal_registers = InternalRegisters(instructions)
		self.cycles = []

	def get_pipeline(self):
		end = False
		start = True

		while not end:
			cycle = [None,None,None,None,None]
			self.internal_registers.cascade_all()

			if self.internal_registers.wb.IR != 0:
				self.internal_registers.writeback()
				cycle[4] = 'WB'

				if self.internal_registers.wb.IR == self.instructions[-1]:
					end = True

			if self.internal_registers.mem_wb.IR != 0:
				self.internal_registers.memory_access()
				cycle[3] = 'MEM'

			if self.internal_registers.ex_mem.IR != 0:
				self.internal_registers.execution()
				cycle[2] = 'EX'

			if self.internal_registers.id_ex.IR != 0:
				self.internal_registers.instruction_decode()
				cycle[1] = 'ID'
		
			self.internal_registers.instruction_fetch()
			if self.internal_registers.if_id.IR != 0:
				cycle[0] = 'IF'

			self.cycles.append(cycle)

		print(self.cycles)


if __name__ == '__main__':
	instructions = ['0043082D', '0043082E', '0043082F']
	temp = Pipeline(instructions)
	temp.get_pipeline()