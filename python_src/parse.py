import os
import re
from defs import *
from PyQt4 import QtCore

class SymbolTuple:

	def __init__(self, addr, title, length):
		self.addr = addr
		self.title = title
		self.length = length

def readLines():
	with open(LOG_FILE) as f:
		lines = [line.strip() for line in f]
	return lines

def readFile():
	with open(LOG_FILE) as f:
		lines = f.read().replace('\n', ' ')
	return lines

def clearFile():
	os.remove(LOG_FILE)
	os.open(LOG_FILE, os.O_CREAT)

def parseDisas():
	lines = []
	remaining_lines = []
	with open(DISAS_OFILE) as f:
		line = f.readline()
		while line:
			# Look for =>, indicating start of assembly code
			# Assembly code should be the last thing in the file
			if line.startswith(ASSEMBLY_START):
				lines.append(line.replace(ASSEMBLY_START, "").strip())
				remaining_lines = [ln.lstrip().rstrip('\n') for ln in f.readlines()]
				break
			line = f.readline()
	
	# Must be a QStringList to add to widget - does not support batch append		
	for line in remaining_lines:
		lines.append(line)

	return lines

def parseLineNum():
	lines = readFile()

	line_match = re.match(LINE_NUM_REGEX, lines)
	line_num = line_match.group(1)

	clearFile()

	return line_num

def parsePointers():
	lines = readLines()

	esp_match = re.match(PTR_REGEX, lines[0])
	my_esp = esp_match.group(1)
	ebp_match = re.match(PTR_REGEX, lines[1])
	my_ebp = ebp_match.group(1)

	clearFile()

	return [my_ebp, my_esp]

def parseFrameInfo():
	lines = readFile()

	line_match = re.match(LINE_REGEX, lines)
	line = line_match.group(1)

	bottom_match = re.match(BOTTOM_REGEX, lines)
	bottom = bottom_match.group(1)

	function_match = re.match(FUNCTION_REGEX, lines)
	title = function_match.group(1)

	registers = parseSavedRegisters()

	clearFile()

	return [title, line, bottom, registers]

def parseSavedRegisters():
	registers = []
	lines = readFile()

	registers_match = re.match(SAVED_REG_REGEX, lines)
	register_string = registers_match.group(1)
	register_list = register_string.split(",")

	for reg_item in register_list:
		reg_match = re.match(REG_ADDR_REGEX, reg_item.strip())
		title = reg_match.group(1)
		addr = reg_match.group(2)
		# Hard coding for 64-bit machine (registers are 1 byte)
		reg = SymbolTuple(addr, title, 8)
		registers.append(reg)

	return registers

def parseVals():
	vals = []
	lines = readLines()

	for line in lines:
		val_match = re.match(ADDR_REGEX, line)
		if val_match:
			val = val_match.group(1)
			vals.append(val)

	clearFile()

	return vals

def parseSymbols():
	symbols = []
	lines = readLines()

	for line in lines:
		sym_match = re.match(SYMBOL_REGEX, line)
		if sym_match:
			title = sym_match.group(1)
			addr = sym_match.group(2)
			length = sym_match.group(3)
			sym = SymbolTuple(addr, title, length)
			symbols.append(sym)

	clearFile()

	return symbols

def parseSymbolVals():
	vals = []
	lines = readLines()

	for line in lines:
		val_match = re.match(PRINT_REGEX, line)
		if val_match:
			val = val_match.group(1)
			vals.append(val)

	clearFile()

	return vals

def parseRegisterVals():
	vals = []
	lines = readLines()

	for line in lines:
		val_match = re.match(PRINT_REGISTER_REGEX, line)
		if val_match:
			val = val_match.group(1)
			vals.append(val)

	clearFile()

	return vals
