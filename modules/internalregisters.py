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
		self.NPC = 0

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
		self.is_forward = False
		self.is_stall = False
		self.stall_jump = False
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
		self.ex_mem.NPC = self.id_ex.NPC

	def cascade_ex_to_mem(self):
		self.mem_wb.IR = self.ex_mem.IR
		self.mem_wb.ALU = self.ex_mem.ALU

	def cascade_mem_to_wb(self):
		self.wb.IR = self.mem_wb.IR

	def check_instruction(self, opcode):
		if opcode[26:32] == '101101' or opcode[26:32] == '101010': #register-to-register
			return 'Register'
		elif opcode[0:6] == '011001' or opcode[0:6] == '001110': #DADDIU instruction
			return 'Immediate'
		elif opcode[0:6] == '110111': #ld instruction
			return 'Load'
		elif opcode[0:6] == '111111': #sd instruction
			return 'Store'
		elif opcode[0:6] == '000001': #bltz instruction
			return 'Jump'

	def check_forwarding(self, current_opcode, next_opcode):
		self.is_stall = False
		self.is_forward = False

		if self.check_instruction(current_opcode) == 'Register':
			if self.check_instruction(next_opcode) == 'Register':
				
				if current_opcode[16:21] == next_opcode[6:11] or current_opcode[16:21] == next_opcode[11:16]:
					self.is_forward = True
				else:
					self.is_forward = False
			elif self.check_instruction(next_opcode) == 'Immediate':
				if current_opcode[16:21] == next_opcode[6:11]:
					self.is_forward = True
				else:
					self.is_forward = False
			elif self.check_instruction(next_opcode) == 'Store':
				if current_opcode[16:21] == next_opcode[11:16] or current_opcode[16:21] == next_opcode[6:11]:
					self.is_forward = True
				else:
					self.is_forward = False
			elif self.check_instruction(next_opcode) == 'Load':
				if current_opcode[16:21] == next_opcode[6:11]:
					self.is_forward = True
				else:
					self.is_forward = False
			elif self.check_instruction(next_opcode) == 'Jump':
				if current_opcode[16:21] == next_opcode[6:11]:
					self.stall_jump = True
				else:
					self.stall_jump = False

		elif self.check_instruction(current_opcode) == 'Immediate':
			if self.check_instruction(next_opcode) == 'Register':
				if current_opcode[11:16] == next_opcode[6:11] or current_opcode[11:16] == next_opcode[11:16]:
					self.is_forward = True
				else:
					self.is_forward = False
			elif self.check_instruction(next_opcode) == 'Immediate':
				if current_opcode[11:16] == next_opcode[6:11]:
					self.is_forward = True
				else:
					self.is_forward = False
			elif self.check_instruction(next_opcode) == 'Store':
				if current_opcode[11:16] == next_opcode[11:16] or current_opcode[11:16] == next_opcode[6:11]:
					self.is_forward = True
				else:
					self.is_forward = False
			elif self.check_instruction(next_opcode) == 'Load':
				if current_opcode[11:16] == next_opcode[6:11]:
					self.is_forward = True
				else:
					self.is_forward = False
			elif self.check_instruction(next_opcode) == 'Jump':
				if current_opcode[11:16] == next_opcode[6:11]:
					self.stall_jump = True
				else:
					self.stall_jump = False

		elif self.check_instruction(current_opcode) == 'Load':
			if self.check_instruction(next_opcode) == 'Register':
				if current_opcode[11:16] == next_opcode[6:11] or current_opcode[11:16] == next_opcode[11:16]:
					self.is_stall = True
				else:
					self.is_stall = False
			elif self.check_instruction(next_opcode) == 'Immediate':
				if current_opcode[11:16] == next_opcode[11:16]:
					self.is_stall = True
				else:
					self.is_stall = False
			elif self.check_instruction(next_opcode) == 'Store':
				if current_opcode[11:16] == next_opcode[11:16] or current_opcode[11:16] == next_opcode[6:11]:
					self.is_stall = True
				else:
					self.is_stall = False
			elif self.check_instruction(next_opcode) == 'Load':
				if current_opcode[11:16] == next_opcode[6:11]:
					self.is_stall = True
				else:
					self.is_stall = False
			elif self.check_instruction(next_opcode) == 'Jump':
				if current_opcode[11:16] == next_opcode[6:11]:
					self.stall_jump = True
					self.is_stall = True
				else:
					self.stall_jump = False
					self.is_stall = False


		else:
			self.is_forward = False
			self.is_stall = False

	def do_forwarding(self, current_opcode, previous_opcode):
		if self.check_instruction(current_opcode) == 'Register':
			if self.check_instruction(previous_opcode) == 'Register':
				
				if previous_opcode[16:21] == current_opcode[6:11]:
					self.id_ex.A = self.ex_mem.ALU
				elif previous_opcode[16:21] == current_opcode[11:16]:
					self.id_ex.B = self.ex_mem.ALU
			elif self.check_instruction(previous_opcode) == 'Immediate':
				if previous_opcode[11:16] == current_opcode[6:11]:
					self.id_ex.A = self.ex_mem.ALU
				elif previous_opcode[11:16] == current_opcode[11:16]:
					self.id_ex.B = self.ex_mem.ALU

		elif self.check_instruction(current_opcode) == 'Immediate':
			if self.check_instruction(previous_opcode) == 'Register':
				if previous_opcode[16:21] == current_opcode[6:11]:
					self.id_ex.A = self.ex_mem.ALU
			elif self.check_instruction(previous_opcode) == 'Immediate':
				if previous_opcode[11:16] == current_opcode[6:11]:
					self.id_ex.A = self.ex_mem.ALU

		elif self.check_instruction(current_opcode) == 'Store':
			if self.check_instruction(previous_opcode) == 'Register':
				if previous_opcode[16:21] == current_opcode[6:11]:
					self.id_ex.A = self.ex_mem.ALU
				elif previous_opcode[16:21] == current_opcode[11:16]:
					self.id_ex.B = self.ex_mem.ALU
			elif self.check_instruction(previous_opcode) == 'Immediate':
				if previous_opcode[11:16] == current_opcode[6:11]:
					self.id_ex.A = self.ex_mem.ALU
				elif previous_opcode[11:16] == current_opcode[11:16]:
					self.id_ex.B = self.ex_mem.ALU

		elif self.check_instruction(current_opcode) == 'Load':
			if self.check_instruction(previous_opcode) == 'Register':
				if previous_opcode[16:21] == current_opcode[6:11]:
					self.id_ex.A = self.id_ex.ALU
			elif self.check_instruction(previous_opcode) == 'Immediate':
				if previous_opcode[11:16] == current_opcode[6:11]:
					self.id_ex.A = self.id_ex.ALU

	def execution_redecode(self):
		self.id_ex.A = self.registers.R[int(bin(int(self.id_ex.IR,16))[2:].zfill(32)[6:11],2)]
		self.id_ex.B = self.registers.R[int(bin(int(self.id_ex.IR,16))[2:].zfill(32)[11:16],2)]		


	def instruction_fetch(self):
		self.is_compact = False
		if self.if_id.PC/4 > len(self.instructions)-1:
			self.if_id.IR = 0
			return False
		else:
			if not self.is_stall and not self.stall_jump:
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
			else:
				self.stall_jump = False
				self.is_stall = False
				#self.if_id.IR = 0
				return False

	def instruction_decode(self):
		print(self.is_compact)
		self.temp_ir = bin(int(str(self.if_id.IR),16))[2:].zfill(32)
		if self.is_compact:
			self.id_ex.IR = 0
			return False
		elif self.if_id.IR != 0 and not self.is_compact and not self.stall_jump:
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
			self.execution_redecode()
			self.temp_ir = bin(int(self.id_ex.IR,16))[2:].zfill(32)
			self.prev_ir = self.instructions[int((self.id_ex.NPC-8)/4)]
			self.prev_ir = bin(int(self.prev_ir,16))[2:].zfill(32)	

			if self.temp_ir[26:32] == '101101': #DADDU instruction
				if not self.is_forward:
					self.ex_mem.ALU = self.id_ex.A + self.id_ex.B
				else:
					self.do_forwarding(self.temp_ir,self.prev_ir)
					print(self.id_ex.A,self.id_ex.B)
					self.ex_mem.ALU = self.id_ex.A + self.id_ex.B
			elif self.temp_ir[0:6] == '011001': #DADDIU instruction
				if not self.is_forward:
					self.ex_mem.ALU = self.id_ex.A + self.id_ex.IMM
				else:
					self.do_forwarding(self.temp_ir,self.prev_ir)
					self.ex_mem.ALU = self.id_ex.A + self.id_ex.IMM
			elif self.temp_ir[0:6] == '001110': #XORI instruction
				if not self.is_forward:
					self.ex_mem.ALU = self.id_ex.A ^ self.id_ex.IMM
				else:
					self.do_forwarding(self.temp_ir,self.prev_ir)
					self.ex_mem.ALU = self.id_ex.A ^ self.id_ex.IMM
			elif self.temp_ir[26:32] == '101010': #SLT instruction
				if not self.is_forward:
					if self.id_ex.A < self.id_ex.B:
						self.ex_mem.ALU = 1
					else:
						self.ex_mem.ALU = 0
				else:
					self.do_forwarding(self.temp_ir,self.prev_ir)
					if self.id_ex.A < self.id_ex.B:
						self.ex_mem.ALU = 1
					else:
						self.ex_mem.ALU = 0
			elif self.temp_ir[0:6] == '110111' or self.temp_ir[0:7] == '111111': #memory reference instructions
				if not self.is_forward:
					self.ex_mem.ALU = self.id_ex.A + self.id_ex.IMM
				else:
					self.do_forwarding(self.temp_ir,self.prev_ir)
					self.ex_mem.ALU = self.id_ex.A + self.id_ex.IMM

			if self.id_ex.NPC/4 <= len(self.instructions)-1:
				self.next_ir = self.instructions[int(self.id_ex.NPC/4)]
				self.next_ir = bin(int(self.next_ir,16))[2:].zfill(32)
				self.check_forwarding(self.temp_ir,self.next_ir)
			
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