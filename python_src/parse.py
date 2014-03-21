import os
import re
from defs import *
from PyQt4 import QtCore

class SymbolTuple:

	def __init__(self, title, addr, length):
		self.title = title
		self.addr = addr
		self.length = length

def parseAssembly(lines):
	assembly = []
	split_lines = lines.split('\n')

	for i in range(0, len(split_lines)):
		if split_lines[i].startswith(ASSEMBLY_START):
			assembly = [line.strip() for line in split_lines[i:]]
			assembly[0] = assembly[0].replace(ASSEMBLY_START, "").strip()
			break

	return assembly

def parseLineNum(lines):
	return regexSearch(LINE_NUM_REGEX, lines)

def parseVal(lines):
	return regexSearch(ADDR_REGEX, lines)

def parseSymbolVal(lines):
	return regexSearch(PRINT_REGEX, lines)

def parseRegisterVal(lines):
	return regexSearch(PRINT_REGISTER_REGEX, lines)

def parseLocalsList(lines):
	return regexFindAll(VAR_REGEX, lines)

def parseFrameInfo(lines):
	title = regexSearch(FUNCTION_REGEX, lines)
	line = regexSearch(LINE_REGEX, lines)
	bottom = regexSearch(BOTTOM_REGEX, lines)

	registers = parseSavedRegisters(lines)

	return [title, line, bottom, registers]

def parseSymbols(lines):
	symbols = []
	matches = regexFindAll(SYMBOL_REGEX, lines)

	for match in matches:
		symbols.append(SymbolTuple(match[0], match[1], match[2]))

	return symbols

def parseSavedRegisters(lines):
	registers = []
	matches = regexFindAll(REG_ADDR_REGEX, lines)

	for match in matches:
		# TODO: fix hard coding for 64-bit machine (registers are 1 byte)
		registers.append(SymbolTuple(match[0], match[1], 8))

	return registers

def regexSearch(regex, lines):
	match = re.search(regex, lines)
	if match:
		return match.group(1)

		# TODO: error handling
	return -1

def regexFindAll(regex, lines):
	match_list = []

	matches = re.findall(regex, lines)
	if matches:
		for match in matches:
			match_list.append(match)

	return match_list
