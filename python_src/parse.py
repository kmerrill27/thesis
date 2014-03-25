import os
import re
from defs import *
from PyQt4 import QtCore

class SymbolTuple:

	def __init__(self, title, addr, length):
		self.title = title
		self.addr = addr
		self.length = length

class VarTuple:

	def __init__(self, title, value):
		self.title = title
		self.value = value

def parseAssembly(lines):
	assembly = []
	split_lines = lines.replace(ASSEMBLER_DUMP, "").strip().split('\n')

	for i in range(0, len(split_lines)):
		if split_lines[i].startswith(ASSEMBLY_START):
			assembly = [line.strip() for line in split_lines[i:]]
			assembly[0] = assembly[0].replace(ASSEMBLY_START, "").strip()
			break

	return assembly

def parseArchitecture(lines):
	return regexSearch(ARCH_REGEX, lines)

def parsePopAddress(lines):
	return regexSearch(POP_ADDR_REGEX, lines)

def parseExitCode(lines):
	return regexSearch(EXIT_REGEX, lines)

def parseLineAndAssembly(lines):
	match = re.search(LINE_NUM_AND_ASSEMBLY_REGEX, lines)
	if match:
		# line number, assembly address start, assembly address end
		return [match.group(1), match.group(2), match.group(3)]

	# TODO: error handling
	return -1

def parseSavedRegisterVal(lines):
	return regexSearch(PRINT_SAVED_REGISTER_REGEX, lines)

def parseRegisterVal(lines):
	return regexSearch(PRINT_REGISTER_REGEX, lines)

def parseVarList(lines):
	return regexFindAll(VAR_NAME_REGEX, lines)

def parseFrameInfo(lines, reg_length):
	title = regexSearch(FUNCTION_REGEX, lines)
	bottom = regexSearch(BOTTOM_REGEX, lines)

	registers = parseSavedRegisters(lines, reg_length)

	return [title, bottom, registers]

def parseSavedRegisters(lines, reg_length):
	registers = []
	matches = regexFindAll(REG_ADDR_REGEX, lines)

	for match in matches:
		registers.append(SymbolTuple(match[0], match[1], reg_length))

	return registers

def parseReturnAddress(addr):
	return regexSearch(RETURN_ADDRESS_REGEX, addr)

def parseHitBreakpointNum(lines):
	return regexSearch(BREAKPOINT_HIT_REGEX, lines)

def parseSetBreakpointNum(lines):
	return regexSearch(BREAKPOINT_NUM_REGEX, lines)

def parseStructCheck(addr):
	return regexSearch(STRUCT_REGEX, addr)

def parseInMainCheck(lines):
	# Returns none if not in main
	return re.search(IN_MAIN, lines)

def parseReturnCheck(lines):
	retval = regexSearch(RETURN_REGEX, lines)
	# Returned with value
	if retval:
		return [True, retval]

	hitBreakpoint = re.search(BREAKPOINT_REGEX, lines)
	# Did not return
	if hitBreakpoint:
		return [False, None]	

	# Returned with no value
	return [True, None]

def parseValue(lines):
	return regexSearch(VAL_REGEX, lines)

def parseAddress(lines):
	return regexSearch(ADDRESS_REGEX, lines)

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
