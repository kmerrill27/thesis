import pexpect
from defs import *
from parse import *

# What if program needs user input?

gdb_process = None

def gdbInit():
	# Open child bash process
	gdb_process = pexpect.spawn('bash')
	gdb_process.expect(BASH_PROMPT)
	gdb_process.sendline(GDB_INIT_CMD.format(INIT_FILE, C_OUT))
	gdb_process.expect(GDB_PROMPT)

	# Set up logging to file
	gdb_process.sendline(SET_LOG_FILE.format(LOG_FILE))
	gdb_process.expect(GDB_PROMPT)
	gdb_process.sendline(RUN)
	gdb_process.expect(GDB_PROMPT)
	gdb_process.sendline(SET_LOG_ON)
	gdb_process.expect(OUTPUT_REDIRECT.format(LOG_FILE))
	gdb_process.sendline(SRC_LINE)
	gdb_process.expect(GDB_PROMPT)

	line_num = parseLineNum()

	gdbFunctionStep()
	# Set up initial stack
	# Return current line

	return line_num

def gdbLineStep():
	gdb_process.sendline(LINE_STEP)
	gdb_process.expect(GDB_PROMPT)
	# Update stack args - check if hits breakpoint
	# If hits breakpoint, in new function - update stack
	# Check if finished

def gdbFunctionStep():
	#gdb_process.sendline(FUNCTION_STEP)
	#gdb_process.expect(GDB_PROMPT)

	gdb_process.sendline(FUNCTION_SCRIPT)
	gdb_process.expect(GDB_PROMPT)

	# title = factorial (0)
	[title, line, my_ebp, my_esp, registers] = parseFrameInfo()

	frame = StackFrame(title, my_ebp, my_esp)

	for reg in registers:

		if reg.title in BASE_POINTERS:
			reg.title = "Callee " + reg.title
		elif reg.title in STACK_POINTERS:
			reg.title = "Return address"
		item = FrameItem(reg.title, reg.addr)
		frame.addItem(item)

		gdb_process.sendline(VAL_AT_ADDR.format(item.addr))
		gdb_process.expect(GDB_PROMPT)

	reg_vals = parseVals()

	assert(len(registers) == len(reg_vals))

	for i in range(0, len(frame.items)):
		frame.items[len(frame.items) - 1 - i].value = reg_vals[i]

	title = frame.title.split()
	gdb_process.sendline(INFO_SCOPE.format(title[0]))
	gdb_process.expect(GDB_PROMPT)

	symbols = parseSymbols()
	for sym in symbols:
		item = FrameItem(sym.title, frame.frame_ptr + sym.offset)
		frame.addItem(item)

		gdb_process.sendline(VAL_AT_ADDR.format(item.addr))
		gdb_process.expect(GDB_PROMPT)

	sym_vals = parseVals()

	assert(len(symbols) == len(sym_vals))

	for i in range(0, len(symbols)):
		frame.items[len(symbols) - 1 - i].value = sym_vals[i]

	return [frame, line]

	# Update stack
	# Check if finished

def gdbRun():
	gdb_process.sendline(REMOVE_BR)
	gdb_process.expect(GDB_PROMPT)
	gdb_process.sendline(CONTINUE)
	gdb_process.expect(GDB_PROMPT)
	# Get result from log

def gdbReset():
	gdb_process.close()
	init_gdb()
	# Clear stack
