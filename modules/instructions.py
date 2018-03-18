import re

class ErrorCheck:

	def __init__(self):
		self.error = False

	def valid_r_type_instruction(self,instruction):
		if 'DADDU' in instruction or 'daddu' in instruction:
			return True
		elif 'SLT' in instruction or 'slt' in instruction:
			return True
		else:
			return False

	def valid_r_type_syntax(self,instruction):
		if re.search(r'((R|r)[0-9]|(R|r)[1-2][0-9]|(R|r)3[0-1]),(\s)*((R|r)[0-9]|(R|r)[1-2][0-9]|(R|r)3[0-1]),(\s)*((R|r)[0-9]|(R|r)[1-2][0-9]|(R|r)3[0-1])(\s)*$',instruction) is None:
			return False
		else:
			return True

	def valid_i_type_instruction(self,instruction):
		if 'DADDIU' in instruction or 'daddiu' in instruction:
			return True
		elif 'XORI' in instruction or 'xori' in instruction:
			return True
		else:
			return False

	def valid_i_type_syntax(self,instruction):
		if re.search(r'((R|r)[0-9]|(R|r)[1-2][0-9]|(R|r)3[0-1]),(\s)*((R|r)[0-9]|(R|r)[1-2][0-9]|(R|r)3[0-1]),(\s)*#\d{4}(\s)*$',instruction) is None:
			return False
		else:
			return True

	def valid_memory_reference_instruction(self,instruction):
		if 'LD' in instruction or 'ld' in instruction:
			return True
		elif 'SD' in instruction or 'sd' in instruction:
			return True
		else:
			return False

	def valid_memory_reference_syntax(self,instruction):
		if re.search(r'((R|r)[0-9]|(R|r)[1-2][0-9]|(R|r)3[0-1]),(\s)*\d{4}\(((R|r)[0-9]|(R|r)[1-2][0-9]|(R|r)3[0-1])\)(\s)*$',instruction) is None:
			return False
		else:
			return True

	def valid_bltz_instruction(self, instruction):
		if re.search(r'((R|r)[0-9]|(R|r)[1-2][0-9]|(R|r)3[0-1]),(\s)*\w*(\s)*$',instruction) is None:
			return False
		else:
			return True

	def valid_bc_instruction(self, instruction):
		if re.search(r'(BC|bc) (\s)*\w*(\s)*$',instruction) is None:
			return False
		else:
			return True

	def valid_branch_syntax(self, instruction):
		if 'BC' in instruction or 'bc' in instruction:
			return True
		elif 'BLTZ' in instruction or 'bltz' in instruction:
			return True
		else:
			return False

class Opcode:

	def __init__(self, instruction):
		self.opcode = 0
		self.error_check = ErrorCheck()
		self.instructions = instruction

	def to_binary(self,register):
		return bin(int(register[1:]))[2:].zfill(5)

	def to_hex(self,opcode):
		return hex(int(opcode,2))[2:].zfill(8).upper()

	def r_type(self,instruction):
		temp = instruction.split(',')
		match = list(map(lambda x: re.search(r'(R|r)[0-9]$|(R|r)[1-2][0-9]$|(R|r)3[0-1]$',x),temp))
		#(rs,rt,rd)
		return (self.to_binary(match[1].group(0)),self.to_binary(match[2].group(0)),self.to_binary(match[0].group(0)))

	def i_type(self,instruction):
		temp = instruction.split(',')
		rt = re.search(r'(R|r)[0-9]$|(R|r)[1-2][0-9]$|(R|r)3[0-1]$',temp[0])
		rs = re.search(r'(R|r)[0-9]$|(R|r)[1-2][0-9]$|(R|r)3[0-1]$',temp[1])
		immediate = bin(int(temp[2][2:],16))[2:].zfill(16)

		return (self.to_binary(rs.group(0)),self.to_binary(rt.group(0)),immediate)

	def memory_reference(self,instruction):
		temp = instruction.split(',')
		rt = re.search(r'(R|r)[0-9]$|(R|r)[1-2][0-9]$|(R|r)3[0-1]$',temp[0])
		rt = rt.group(0)
		temp = temp[1].split('(')
		offset = bin(int(temp[0][1:],16))[2:].zfill(16)
		base = re.search(r'(R|r)[0-9]|(R|r)[1-2][0-9]|(R|r)3[0-1]',temp[1])
		base = base.group(0)
		return (self.to_binary(base),self.to_binary(rt),offset)

	def branch_bltz(self, instruction):
		temp = instruction.split(',')
		rs = re.search(r'(R|r)[0-9]$|(R|r)[1-2][0-9]$|(R|r)3[0-1]$',temp[0])
		rs = rs.group(0)
		temp1 = [i for i, j in enumerate(self.instructions) if temp[1].lstrip() in j]
		if len(temp1) > 1:
			offset = temp1[1] - (temp1[0]+1)
			return (self.to_binary(rs),bin(offset)[2:].zfill(16))
		else:
			return False

	def branch_bc(self, instruction):
		temp = instruction.split(' ')
		temp1 = [i for i, j in enumerate(self.instructions) if temp[1].lstrip() in j]
		if len(temp1) > 1:
			offset = temp1[1] + (temp1[0]+1)
			return bin(offset)[2:].zfill(26)
		else:
			return False

	def get_opcode(self,instruction):
		if 'DADDU' in instruction or 'daddu' in instruction:
			if self.error_check.valid_r_type_syntax(instruction):
				opcode = '000000' + self.r_type(instruction)[0] + self.r_type(instruction)[1] + self.r_type(instruction)[2] + '00000101101'
			else:
				return 'Invalid Syntax ' + instruction
		elif 'SLT' in instruction or 'slt' in instruction:
			if self.error_check.valid_r_type_syntax(instruction):
				opcode = '000000' + self.r_type(instruction)[0] + self.r_type(instruction)[1] + self.r_type(instruction)[2] + '00000101010'
			else:
				return 'Invalid Syntax ' + instruction
		elif 'DADDIU' in instruction or 'daddiu' in instruction:
			if self.error_check.valid_i_type_syntax(instruction):
				opcode = '011001' + self.i_type(instruction)[0] + self.i_type(instruction)[1] + self.i_type(instruction)[2]
			else:
				return 'Invalid Syntax ' + instruction
		elif 'XORI' in instruction or 'xori' in instruction:
			if self.error_check.valid_i_type_syntax(instruction):
				opcode = '001110' + self.i_type(instruction[0]) + self.i_type(instruction[1]) + self.i_type(instruction[2])
			else:
				return 'Invalid Syntax ' + instruction
		elif 'LD' in instruction or 'ld' in instruction:
			if self.error_check.valid_memory_reference_syntax(instruction):
				opcode = '110111' + self.memory_reference(instruction)[0] + self.memory_reference(instruction)[1] + self.memory_reference(instruction)[2]
			else:
				return 'Invalid Syntax ' + instruction
		elif 'SD' in instruction or 'sd' in instruction:
			if self.error_check.valid_memory_reference_syntax(instruction):
				opcode = '111111' + self.memory_reference(instruction)[0] + self.memory_reference(instruction)[1] + self.memory_reference(instruction)[2]
			else:
				return 'Invalid Syntax ' + instruction
		elif 'BLTZ' in instruction or 'bltz' in instruction:
			if self.error_check.valid_bltz_instruction(instruction):
				if self.branch_bltz(instruction) is not False:
					opcode = '000001' + self.branch_bltz(instruction)[0] + '00000' + self.branch_bltz(instruction)[1]
				else:
					return 'Offset not found!'
			else:
				return 'Invalid Syntax ' + instruction
		elif 'BC' in instruction or 'bc' in instruction:
			if self.error_check.valid_bc_instruction(instruction):
				if self.branch_bc(instruction) is not False:
					opcode = '110010' + self.branch_bc(instruction)
				else:
					return 'Offset not found!'
			else:
				return 'Invalid Syntax ' + instruction
		else:
			return 'Unknown Instruction ' + instruction

		return self.to_hex(opcode)



if __name__ == '__main__':
	instruction = ['BLTZ R1,        L1','NOP','L1: DADDU R1,             R2,              R3']
	temp = Opcode(instruction)
	print(temp.get_opcode(instruction[0]))
