
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
		self.cascade_if_to_id()
		self.cascade_id_to_ex()
		self.cascade_ex_to_mem()
		self.cascade_mem_to_wb()

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
		self.if_id.IR = self.instructions
		self.if_id.PC += 4
		self.if_id.NPC += 4

	def instruction_decode(self):
		pass

	def execution(self):
		pass

	def memory_access(self):
		pass

	def writeback(self):
		pass