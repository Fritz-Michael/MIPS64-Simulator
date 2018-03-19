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
		self.registers = Registers()
		self.is_compact = False
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
		self.is_compact = False
		if self.if_id.PC/4 > len(self.instructions)-1:
			self.if_id.IR = 0
			return False
		else:
			self.temp_ir = bin(int(str(self.if_id.IR),16))[2:].zfill(32)
			self.if_id.IR = self.instructions[int(self.if_id.PC/4)]
			#if branch instruction
			if (self.temp_ir[0:6] == '000001' and self.registers.R[int(self.temp_ir[2:].zfill(32)[6:11],2)] < 0) or self.temp_ir[0:6] == '110010':
				offset = int(self.temp_ir[2:].zfill(32)[16:32],2) << 2
				self.if_id.PC = offset + self.if_id.NPC
				self.if_id.NPC = self.if_id.PC

				if self.temp_ir[0:6] == '110010':
					self.is_compact = True
			else:
				self.if_id.NPC += 4
				self.if_id.PC += 4
			return True

	def instruction_decode(self):
		self.temp_ir = bin(int(str(self.if_id.IR),16))[2:].zfill(32)
		if self.is_compact:
			self.id_ex.IR = 0
			return False
		elif self.if_id.IR != 0:
			self.id_ex.A = self.registers.R[int(bin(int(self.if_id.IR,16))[2:].zfill(32)[6:11],2)]
			self.id_ex.B = self.registers.R[int(bin(int(self.if_id.IR,16))[2:].zfill(32)[11:16],2)]
			self.id_ex.IMM = int(bin(int(self.if_id.IR,16))[2:].zfill(32)[16:],2)
			self.cascade_if_to_id()
			return True
		else:
			self.id_ex.IR = 0
			return False

	def execution(self):
		if self.id_ex.IR != 0:
			self.temp_ir = bin(int(self.id_ex.IR,16))[2:].zfill(32)

			if self.temp_ir[26:32] == '101101': #DADDU instruction
				self.ex_mem.ALU = self.id_ex.A + self.id_ex.B
			elif self.temp_ir[0:6] == '011001': #DADDIU instruction
				self.ex_mem.ALU = self.id_ex.A + self.id_ex.IMM
			elif self.temp_ir[0:6] == '001110': #XORI instruction
				self.ex_mem.ALU = self.id_ex.A ^ self.id_ex.IMM 
			elif self.temp_ir[26:32] == '101010': #SLT instruction
				if self.id_ex.A < self.id_ex.B:
					self.ex_mem.ALU = 1
				else:
					self.ex_mem.ALU = 0
			elif self.temp_ir[0:6] == '110111' or self.temp_ir[0:7] == '111111': #memory reference instructions
				self.ex_mem.ALU = self.id_ex.A + self.id_ex.IMM

			self.cascade_id_to_ex()
			return True
		else:
			self.ex_mem.IR = 0
			return False

	def memory_access(self):
		if self.ex_mem.IR != 0:
			self.temp_ir = bin(int(self.ex_mem.IR,16))[2:].zfill(32)

			if self.temp_ir[0:6] == '110111': #load instruction
				self.mem_wb.LMD = None #self.memory[self.ex_mem.ALU]
			elif self.temp_ir[0:6] == '111111': #store instruction
				#self.memory[self.ex_mem.ALU] = self.ex_mem.B
				pass

			self.mem_wb.ALU = self.ex_mem.ALU
			self.cascade_ex_to_mem()
			return True
		else:
			self.mem_wb.IR = 0
			return False

	def writeback(self):
		if self.mem_wb.IR != 0:
			self.temp_ir = bin(int(self.mem_wb.IR,16))[2:].zfill(32)

			if self.temp_ir[0:6] == '011001' or self.temp_ir[0:7] == '001110': #register-to-immediate instructions
				self.registers.R[int(self.temp_ir[2:].zfill(32)[11:16],2)] = self.mem_wb.ALU
			elif self.temp_ir[26:32] == '101101' or self.temp_ir[26:32] == '101010': #register-to-register instructions
				self.registers.R[int(self.temp_ir[2:].zfill(32)[16:21],2)] = self.mem_wb.ALU
			elif self.temp_ir[0:6] == '110111': #load instruction
				self.registers.R[int(self.temp_ir[2:].zfill(32)[11:16],2)] = self.mem_wb.LMD

			self.cascade_mem_to_wb()
			return True
		else:
			self.wb.IR = 0
			return False