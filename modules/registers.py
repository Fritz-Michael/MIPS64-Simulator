#Contains the values of the registers

class Registers:
	
	def __init__(self):
		self.reinit()

	def reinit(self):
		self.R = [0 for x in range(32)]
