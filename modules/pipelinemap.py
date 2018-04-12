# try:
from modules.internalregisters import *
from modules.instructions import *
# except:
# 	from internalregisters import *
# 	from instructions import *

class Pipeline:

	def __init__(self, instructions, opcode):
		self.instructions = instructions
		self.opcode = opcode
		self.internal_registers = InternalRegisters(opcode)
		self.cycles = []
		self.values = []
		self.registers = []
		self.memory = []

	def get_pipeline(self):

		end = False
		while not end:
			# print(self.cycles)
			cycle = [None,None,None,None,None]
			value = []
			if self.internal_registers.writeback():
				cycle[4] = 'WB'
				if self.internal_registers.wb.IR == self.opcode[-1]:
					end = True
			value.append(self.internal_registers.wb.IR)
			if self.internal_registers.memory_access():
				cycle[3] = 'MEM'
			value.append(self.internal_registers.mem_wb.IR)
			if self.internal_registers.execution():
				cycle[2] = 'EX'
			value.append(self.internal_registers.ex_mem.IR)
			if self.internal_registers.instruction_decode():
				cycle[1] = 'ID'
			value.append(self.internal_registers.id_ex.IR)
			if self.internal_registers.instruction_fetch():
				cycle[0] = 'IF'
			value.append(self.internal_registers.if_id.IR)
			self.cycles.append(cycle)
			self.values.append(value)
			self.registers.append(self.internal_registers.registers)
			self.memory.append(self.internal_registers.memory)
		print(self.cycles)
		#print(self.internal_registers.memory.memory[0]['0x7'])


if __name__ == '__main__':
	#instructions = ['DADDIU R1, R0, #fffe','SD R1, 0000(R0)', 'LD R2, 0000(R0)']
	#instructions = ['DADDIU R1, R0, #0003','SD R1, 0000(R0)', 'LD R2, 0000(R0)','DADDU R3, R2, R4', 'DADDU R5, R6, R7']
	#instructions = ['BC L1','DADDU R1, R2, R3','L1: DADDIU R2, R0, #0004']
	#instructions = ['DADDIU R1, R0, #FFFF','BLTZ R1, L1','DADDIU R3, R0, #0003','L1: DADDIU R2, R0, #0001']
	instructions = ['DADDIU R1, R0, #fffe','SD R1, 0000(R0)','LD R1, 0000(R0)','BLTZ R1, L1', 'DADDIU R2, R3, #FFFF', 'L1: DADDIU R4, R5, #0000']
	opcode = Opcode(instructions)
	ins = list(map(lambda x: opcode.get_opcode(x),instructions))
	print(ins)
	temp = Pipeline(instructions, ins)
	temp.get_pipeline()
	print(temp.internal_registers.registers.R)
	print(instructions)
