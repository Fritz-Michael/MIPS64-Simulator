import re

class Opcode:

	def __init__(self):
		self.opcode = 0

	def to_binary(self,register):
		return bin(int(register[1:]))[2:].zfill(5)
	
	def to_hex(self,opcode):
		return hex(int(opcode,2))[2:].zfill(8).upper()

	def r_type(self,instruction):
		temp = instruction.split(',')
		match = list(map(lambda x: re.search(r'R[0-31]',x),temp))
		#(rs,rt,rd)
		return (self.to_binary(match[1].group(0)),self.to_binary(match[2].group(0)),self.to_binary(match[0].group(0)))

	def i_type(self,instruction):
		temp = instruction.split(',')
		rt = re.search(r'R[0-31]',temp[0])
		rs = re.search(r'R[0-31]',temp[1])
		immediate = bin(int(temp[2][2:],16))[2:].zfill(16)

		return (self.to_binary(rs.group(0)),self.to_binary(rt.group(0)),immediate)

	def memory_reference(self,instruction):
		temp = instruction.split(',')
		rt = re.search(r'R[0-31]',temp[0])
		rt = rt.group(0)
		temp = temp[1].split('(')
		offset = bin(int(temp[0][1:],16))[2:].zfill(16)
		base = re.search(r'R[0-31]',temp[1])
		base = base.group(0)
		return (self.to_binary(base),self.to_binary(rt),offset)

	def get_opcode(self,instruction):
		if 'DADDU' in instruction:
			opcode = '000000' + self.r_type(instruction)[0] + self.r_type(instruction)[1] + self.r_type(instruction)[2] + '00000101101'
		elif 'SLT' in instruction:
			opcode = '000000' + self.r_type(instruction)[0] + self.r_type(instruction)[1] + self.r_type(instruction)[2] + '00000101010'
		elif 'DADDIU' in instruction:
			opcode = '011001' + self.i_type(instruction[0]) + self.i_type(instruction[1]) + self.i_type(instruction[2])
		elif 'XORI' in instruction:
			opcode = '001110' + self.i_type(instruction[0]) + self.i_type(instruction[1]) + self.i_type(instruction[2])
		elif 'LD' in instruction:
			opcode = '110111'
		elif 'SD' in instruction:
			opcode = '111111'

		return self.to_hex(opcode)





