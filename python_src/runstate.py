import pexpect
from defs import *
from parse import *
from stackframe import *

# What if program needs user input?

class GDBProcess:

	def __init__(self):
		self.process = None

	# Must reset logging after each log file open
	# Call after every parse
	def resetLogging(self):
		self.process.sendline(SET_LOG_OFF)
		self.process.expect(DONE_LOGGING.format(LOG_FILE))
		self.process.sendline(SET_LOG_ON)
		self.process.expect(OUTPUT_REDIRECT.format(LOG_FILE))

	# Hacky way to make sure output is flushed to file
	# Call before every parse
	def flushToLogFile(self):
		self.process.sendline(TRACE_ON)
		self.process.expect(GDB_PROMPT)
		self.process.sendline(TRACE_OFF)
		self.process.expect(GDB_PROMPT)

	def gdbInit(self):
		# Reset log file
		clearFile()

		# Open child bash process
		self.process = pexpect.spawn('bash')
		self.process.expect(BASH_PROMPT)
		self.process.sendline(GDB_INIT_CMD.format(INIT_FILE, C_OUT))
		self.process.expect(GDB_PROMPT)

		# Set up logging to file
		self.process.sendline(SET_LOG_FILE.format(LOG_FILE))
		self.process.expect(GDB_PROMPT)
		self.process.sendline(RUN)
		self.process.expect(GDB_PROMPT)
		self.process.sendline(SET_LOG_ON)
		self.process.expect(OUTPUT_REDIRECT.format(LOG_FILE))
		self.process.sendline(SRC_LINE)
		self.process.expect(GDB_PROMPT)

		self.process.sendline("continue")
		self.process.expect(GDB_PROMPT)

		line_num = parseLineNum()

		# TODO: Set up initial stack

		return line_num

	def gdbLineStep(self):
		self.resetLogging()

		self.process.sendline(LINE_STEP)
		self.process.expect(GDB_PROMPT)
		# Update stack args - check if hits breakpoint
		# If hits breakpoint, in new function - update stack
		# Check if finished

	def gdbFunctionStep(self):
		self.process.sendline(FUNCTION_STEP)
		self.process.expect(GDB_PROMPT)

		self.resetLogging()

		self.process.sendline(INFO_FRAME)
		self.process.expect(GDB_PROMPT)

		self.flushToLogFile()
		[title, line, bottom, registers] = parseFrameInfo()
		self.resetLogging()

		self.process.sendline(PRINT_REGISTER.format(BASE_POINTER))
		self.process.expect(GDB_PROMPT)
		self.process.sendline(PRINT_REGISTER.format(STACK_POINTER))
		self.process.expect(GDB_PROMPT)

		self.flushToLogFile()
		[my_ebp, my_esp] = parseRegisterVals()
		self.resetLogging()

		frame = StackFrame(title, my_ebp, my_esp, bottom)

		for reg in registers:

			if reg.title in BASE_POINTERS:
				reg.title = "Callee " + reg.title
			elif reg.title in STACK_POINTERS:
				reg.title = "Return address"
			item = FrameItem(reg.title, reg.addr, reg.length, None)
			frame.addItem(item)

			self.process.sendline(VAL_AT_ADDR.format(1, item.addr))
			self.process.expect(GDB_PROMPT)

		self.flushToLogFile()
		reg_vals = parseVals()
		self.resetLogging()

		assert(len(registers) == len(reg_vals))

		for i in range(0, len(frame.items)):
			frame.items[len(frame.items) - 1 - i].value = reg_vals[i]

		self.process.sendline(INFO_SCOPE.format(frame.title))
		self.process.expect(GDB_PROMPT)

		self.flushToLogFile()
		symbols = parseSymbols()
		self.resetLogging()

		for sym in symbols:
			#item = FrameItem(sym.title, "$ebp+" + sym.addr, sym.bytes, None)
			item = FrameItem(sym.title, hex(int(frame.frame_ptr, 16) + int(sym.addr)), sym.length, None)
			frame.addItem(item)

			#self.process.sendline(VAL_AT_ADDR.format(item.bytes, item.addr))
			self.process.sendline(PRINT_SYMBOL.format(sym.title))
			self.process.expect(GDB_PROMPT)

		self.flushToLogFile()
		sym_vals = parseSymbolVals()
		self.resetLogging()

		assert(len(symbols) == len(sym_vals))

		for i in range(0, len(symbols)):
			frame.items[len(symbols) - 1 - i].value = sym_vals[i]

		return [frame, line]

		# TODO: Check if finished

	def gdbRun(self):
		self.resetLogging()

		self.process.sendline(REMOVE_BR)
		self.process.expect(GDB_PROMPT)
		self.process.sendline(CONTINUE)
		self.process.expect(GDB_PROMPT)
		# Get result from log

	def gdbReset(self):
		self.process.close()
		self.gdbInit()
		# Clear stack
