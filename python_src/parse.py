import re
import string

from defs import *
from parsedefs import *

class SymbolTuple:
	""" Representation of a symbol with name and address """

	def __init__(self, title, addr):
		self.title = title
		self.addr = addr

def parseArchitecture(lines):
	""" Get x86 machine architecture: 32- or 64- bit """
	return regexSearch(ARCH_REGEX, lines)

def parseFrameInfo(lines):
	""" Get function name, base address, and saved registers for new frame """
	title = regexSearch(FUNCTION_REGEX, lines)
	bottom = regexSearch(BOTTOM_REGEX, lines)

	registers = parseSavedRegisters(lines)

	return [title, bottom, registers]

def parseLineAndAssembly(lines):
	""" Get current source line and corresponding assembly start and end addresses """
	match = re.search(LINE_NUM_AND_ASSEMBLY_REGEX, lines)
	if match:
		# line number, assembly address start, assembly address end
		return [match.group(1), match.group(2), match.group(3)]

	return -1

def parseAssembly(lines):
	""" Get to-be executed assembly instructions for source line """
	assembly = []
	split_lines = lines.replace(ASSEMBLER_DUMP, "").strip().split('\n')

	for i in range(0, len(split_lines)):
		# Current assembly instruction marked with "=>"
		if split_lines[i].startswith(ASSEMBLY_START):
			# Take all instructions following current instruction
			assembly = [line.strip() for line in split_lines[i:]]
			assembly[0] = assembly[0].replace(ASSEMBLY_START, "").strip()
			break

	return assembly

def parseVarList(lines):
	""" Get names of variables from 'info args' or 'info locals' call """
	return regexFindAll(VAR_NAME_REGEX, lines)

def parseAddress(lines):
	""" Get address of info-ed var """
	return regexSearch(ADDRESS_REGEX, lines)

def parseValue(lines):
	""" Get value of printed var """
	return regexSearch(VAL_REGEX, lines)

def parseRegisterValue(lines):
	""" Get value of register """
	return regexSearch(PRINT_REGISTER_REGEX, lines)

def parseSavedRegisterValue(lines):
	""" Get value of saved register """
	return regexSearch(PRINT_SAVED_REGISTER_REGEX, lines)

def parseSavedRegisters(lines):
	""" Get name and address of saved registers """
	registers = []
	matches = regexFindAll(REG_ADDR_REGEX, lines)

	for match in matches:
		registers.append(SymbolTuple(match[0], match[1]))

	return registers

def parseStructCheck(value):
	""" Check if symbol is a struct """
	match = re.search(STRUCT_REGEX, value)
	if match:
		# e.x. ["(struct node *) ", "0x000"]
		return [match.group(1) + " ", match.group(2)]
	else:
		# Symbol is not a struct
		return [NON_STRUCT, value]

def parseInstruction(lines):
	""" Get single assembly instruction from x/i command """
	return string.join(regexSearch(ASSEMBLY_INSTR_REGEX, lines).split(), "   ")

def parseSetBreakpointNum(lines):
	""" Get number of just set breakpoint """
	return regexSearch(BREAKPOINT_NUM_REGEX, lines)

def parseHitBreakpointNum(lines):
	""" Get number of just hit breakpoint """
	return regexSearch(BREAKPOINT_HIT_REGEX, lines)

def parseReturnAddress(addr):
	""" Get address from address pointer definition """
	return regexSearch(RET_ADDR_REGEX, addr)

def parseMainReturnAddress(lines):
	""" Get address of instruction right before retq """
	return regexSearch(POP_ADDR_REGEX, lines)

def parseExitStatus(lines):
	""" Get exit status of completed program execution """
	return regexSearch(EXIT_REGEX, lines)

def parseFunctionStepInMainCheck(lines):
	""" For function step only: check if function in main """
	return re.search(IN_MAIN, lines)

def parseFunctionStepReturnCheck(lines):
	""" For function step only: check if function returned """
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

def regexSearch(regex, lines):
	""" Get first match for regex """
	match = re.search(regex, lines)
	if match:
		return match.group(1)

	return None

def regexFindAll(regex, lines):
	""" Get list of all matches for regex """
	match_list = []

	matches = re.findall(regex, lines)
	if matches:
		for match in matches:
			match_list.append(match)

	return match_list
