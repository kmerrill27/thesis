import os
import re
from defs import *
from PyQt4 import QtCore

class SymbolTuple:

	def __init__(self, title, addr, length):
		self.title = title
		self.addr = addr
		self.length = length

class LocalTuple:

	def __init__(self, title, value):
		self.title = title
		self.value = value

def parseAssembly(lines):
	assembly = []
	split_lines = lines.replace(ASSEMBLER_DUMP, "").split('\n')

	for i in range(0, len(split_lines)):
		if split_lines[i].startswith(ASSEMBLY_START):
			assembly = [line.strip() for line in split_lines[i:]]
			assembly[0] = assembly[0].replace(ASSEMBLY_START, "").strip()
			break

	return assembly

def parseArchitecture(lines):
	return regexSearch(ARCH_REGEX, lines)

def parseLineAndAssembly(lines):
	match = re.search(LINE_NUM_AND_ASSEMBLY_REGEX, lines)
	if match:
		# line number, assembly address start, assembly address end
		return [match.group(1), match.group(2), match.group(3)]

	# TODO: error handling
	return -1

def parseLineNum(lines):
	return regexSearch(LINE_NUM_REGEX, lines)

def parseVal(lines):
	return regexSearch(ADDR_REGEX, lines)

def parseSymbolVal(lines):
	return regexSearch(PRINT_REGEX, lines)

def parseSavedRegisterVal(lines):
	return regexSearch(PRINT_SAVED_REGISTER_REGEX, lines)

def parseRegisterVal(lines):
	return regexSearch(PRINT_REGISTER_REGEX, lines)

def parseLocalsList(lines):
	locals_list = []
	print lines
	matches = regexFindAll(LOCAL_REGEX, lines)
	for match in matches:
		locals_list.append(LocalTuple(match[0], match[1]))

	return locals_list

def parseFrameInfo(lines, reg_length):
	title = regexSearch(FUNCTION_REGEX, lines)
	line = regexSearch(LINE_REGEX, lines)
	bottom = regexSearch(BOTTOM_REGEX, lines)

	registers = parseSavedRegisters(lines, reg_length)

	return [title, line, bottom, registers]

def parseSymbols(lines):
	symbols = []
	matches = regexFindAll(SYMBOL_REGEX, lines)

	for match in matches:
		symbols.append(SymbolTuple(match[0], match[1], match[2]))

	return symbols

def parseSavedRegisters(lines, reg_length):
	registers = []
	matches = regexFindAll(REG_ADDR_REGEX, lines)

	for match in matches:
		registers.append(SymbolTuple(match[0], match[1], reg_length))

	return registers

def parseReturnCheck(lines):
	# TODO: FIX THIS
	print lines
	retval = regexSearch(RETURN_REGEX, lines)
	# Returned with value
	if retval:
		return [True, retval]

	returned = re.search(BREAKPOINT_REGEX, lines)
	# Returned with no value
	if returned:
		return [True, None]	

	return [False, None]

def regexSearch(regex, lines):
	match = re.search(regex, lines)
	if match:
		return match.group(1)

	# TODO: error handling
	return None

def regexFindAll(regex, lines):
	match_list = []

	matches = re.findall(regex, lines)
	if matches:
		for match in matches:
			match_list.append(match)

	return match_list
