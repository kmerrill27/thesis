# In GDB: python execfile ("test.py")
# From terminal: gdb -q -x test.py 

#import sys
#import gdb
import re
from parse import *
from defs import *

#gdb.execute("file stackviz")
#br1 = gdb.Breakpoint("1")
#br2 = gdb.Breakpoint("factorial")
#gdb.execute("run")

with open("test.txt") as f:
	lines = f.read().replace('\n', '')

	ebp_match = re.match(ADDR_REGEX, lines)
	my_ebp = ebp_match.group(1)
	esp_match = re.match(ADDR_REGEX, lines)
	my_esp = esp_match.group(1)

	level_match = re.match(LEVEL_REGEX, lines)
	level = level_match.group(1)

	line_match = re.match(LINE_REGEX, lines)
	line = line_match.group(1)

	function_match = re.match(FUNCTION_REGEX, lines)
	function = function_match.group(1)

	title = function + " (" + level + ")"

	registers = []

	registers_match = re.match(SAVED_REG_REGEX, lines)
	register_string = registers_match.group(1)
	register_list = register_string.split(",")

	for reg_item in register_list:
		reg_match = re.match(REG_ADDR_REGEX, reg_item.strip())
		title = reg_match.group(1)
		addr = reg_match.group(2)
		reg = AddressTitleTuple(addr, title)
		registers.append(reg)

print registers

#os.remove("test.txt")
#os.open("test.txt")

