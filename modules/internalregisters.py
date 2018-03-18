from registers import *

class IF_ID:
	
	def __init__(self):
		self.PC = 0
		self.IR = 0
		self.NPC = 0

class ID_EX:

	def __init__(self):
		self.IR = 0
		self.NPC = 0
		self.A = 0
		self.B = 0
		self.IMM = 0

class EX_MEM:

	def __init__(self):
		self.IR = 0
		self.ALU = 0
		self.COND = 0

class MEM_WB:

	def __init__(self):
		self.IR = 0
		self.ALU = 0
		self.LMD = None


class WB:

	def __init__(self):
		self.IR = 0


class InternalRegisters:

	def __init__(self, instructions):
		self.instructions = instructions
		self.if_id = IF_ID()
		self.id_ex = ID_EX()
		self.ex_mem = EX_MEM()
		self.mem_wb = MEM_WB()
		self.wb = WB()

	def cascade_all(self):
		self.cascade_mem_to_wb()
		self.cascade_ex_to_mem()
		self.cascade_id_to_ex()
		self.cascade_if_to_id()

	def cascade_if_to_id(self):
		self.id_ex.IR = self.if_id.IR
		self.id_ex.NPC = self.if_id.NPC

	def cascade_id_to_ex(self):
		self.ex_mem.IR = self.id_ex.IR

	def cascade_ex_to_mem(self):
		self.mem_wb.IR = self.ex_mem.IR
		self.mem_wb.ALU = self.ex_mem.ALU

	def cascade_mem_to_wb(self):
		self.wb.IR = self.mem_wb.IR

	def instruction_fetch(self):
		if self.if_id.PC/4 > len(self.instructions)-1:
			self.if_id.IR = 0
			return False
		else:
			self.if_id.IR = self.instructions[int(self.if_id.PC/4)]
			self.if_id.PC += 4
			self.if_id.NPC += 4
			return True

	def instruction_decode(self):
		if self.if_id.IR != 0:
			self.id_ex.A = hex(int(bin(int(self.if_id.IR,16))[2:].zfill(32)[6:11],2))[2:].zfill(16).upper()
			self.id_ex.B = hex(int(bin(int(self.if_id.IR,16))[2:].zfill(32)[11:16],2))[2:].zfill(16).upper()
			self.id_ex.IMM = hex(int(bin(int(self.if_id.IR,16))[2:].zfill(32)[16:],2))[2:].zfill(16).upper()
			self.cascade_if_to_id()
			return True
		else:
			self.id_ex.IR = 0
			return False

	def execution(self):
		if self.id_ex.IR != 0:
			self.temp_ir = bin(int(self.id_ex.IR,16))[2:].zfill(32)
			if self.temp_ir[26:32] == '101101': #register-to-register
				self.ex_mem.ALU = int(self.id_ex.A,16) + int(self.id_ex.B,16)
				print(self.ex_mem.ALU)
			elif self.temp_ir[0:6] == '011001' or self.temp_ir[0:7] == '001110': #register-to-immediate
				self.ex_mem.ALU = int(self.id_ex.A,16) + int(self.id_ex.IMM,16)
				print('pass reg to imm')
			elif self.temp_ir[26:32] == '101010': #set
				if int(self.id_ex.A,16) < int(self.id_ex.B,16):
					self.ex_mem.ALU = 1
				else:
					self.ex_mem.ALU = 0
				print('pass set')
			elif self.temp_ir[0:6] == '110111' or self.temp_ir[0:7] == '111111': #memory reference
				self.ex_mem.ALU = int(self.id_ex.A,16) + int(self.id_ex.IMM,16)
				print('pass memory reference')
			self.cascade_id_to_ex()
			return True
		else:
			self.ex_mem.IR = 0
			return False

	def memory_access(self):
		if self.ex_mem.IR != 0:
			self.cascade_ex_to_mem()
			return True
		else:
			self.mem_wb.IR = 0
			return False

	def writeback(self):
		if self.mem_wb.IR != 0:
			self.cascade_mem_to_wb()
			return True
		else:
			self.wb.IR = 0
			return False