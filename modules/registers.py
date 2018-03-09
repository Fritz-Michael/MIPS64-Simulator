#Contains the values of the registers

class Registers:
	
	def __init__(self):
		self.R[32] = 0

	def reinit(self):
		self.R[32] = 0