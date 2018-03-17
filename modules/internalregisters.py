
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
		else:
			self.if_id.IR = self.instructions[int(self.if_id.PC/4)]
			self.if_id.PC += 4
			self.if_id.NPC += 4

	def instruction_decode(self):
		#self.cascade_if_to_id()
		self.id_ex.A = hex(int(bin(int(self.if_id.IR,16))[2:].zfill(32)[6:11],2))[2:].zfill(16).upper()
		self.id_ex.B = hex(int(bin(int(self.if_id.IR,16))[2:].zfill(32)[11:16],2))[2:].zfill(16).upper()
		self.id_ex.IMM = hex(int(bin(int(self.if_id.IR,16))[2:].zfill(32)[16:],2))[2:].zfill(16).upper()

	def execution(self):
		if self.ex_mem.IR[0:7] == '': #register-to-register
			pass
		elif self.ex_mem.IR[0:7] == '011001' or self.ex_mem.IR[0:7] == '001110': #register-to-immediate
			pass
		elif self.ex_mem.IR[0:7] == '': #shift
			pass
		elif self.ex_mem.IR[0:7] == '110111' or self.ex_mem.IR[0:7] == '111111': #memory reference
			pass

	def memory_access(self):
		pass

	def writeback(self):
		pass