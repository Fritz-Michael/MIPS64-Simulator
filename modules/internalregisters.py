
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
		self.if_id = IF_ID()
		self.id_ex = ID_EX()
		self.ex_mem = EX_MEM()
		self.mem_wb = MEM_WB()
		self.wb = WB()
