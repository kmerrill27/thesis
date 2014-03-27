from defs import *

class MachineArchitecture:
	""" Representation of machine architecture - 32- or 64-bit x86 """

	def __init__(self):
		self.bits = None # x-bit
		self.reg_length = None # length of register
		self.base_pointer = None # name of base pointer
		self.stack_pointer = None # name of stack pointer
		self.instr_pointer = None # name of instruction pointer

	def setArchitecture(self, bits):
		self.bits = bits
		self.reg_length = bits/8
		self.base_pointer = BASE_POINTERS[bits/32 - 1]
		self.stack_pointer = STACK_POINTERS[bits/32 - 1]
		self.instr_pointer = INSTR_POINTERS[bits/32 - 1]
