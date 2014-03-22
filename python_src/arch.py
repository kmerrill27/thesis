from defs import *

class MachineArchitecture:

	def __init__(self):
		self.bits = None
		self.reg_length = None
		self.base_pointer = None
		self.stack_pointer = None
		self.instr_pointer = None

	def setArchitecture(self, bits):
		self.bits = bits
		self.reg_length = bits/8
		self.base_pointer = BASE_POINTERS[bits/32 - 1]
		self.stack_pointer = STACK_POINTERS[bits/32 - 1]
		self.instr_pointer = INSTR_POINTERS[bits/32 - 1]