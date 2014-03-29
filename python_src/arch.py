from defs import *

class MachineArchitecture:
	""" Representation of machine architecture - 32- or 64-bit x86 """

	def __init__(self, bits):
		self.bits = bits # x-bit
		self.reg_length = bits/8 # length of register
		self.base_pointer = BASE_POINTERS[bits/32 - 1] # name of base pointer
		self.stack_pointer = STACK_POINTERS[bits/32 - 1] # name of stack pointer
		self.instr_pointer = INSTR_POINTERS[bits/32 - 1] # name of instruction pointer
