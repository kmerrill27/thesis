import pexpect
from defs import *
from parse import *
from stackframe import *

# What if program needs user input?

class GDBProcess:

	def __init__(self):
		self.process = None
		self.started = False

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
		print self.process.before.strip()
		self.process.sendline(RUN)
		self.process.expect(GDB_PROMPT)
		print self.process.before.strip()
		self.process.sendline(SET_LOG_ON)
		self.process.expect(OUTPUT_REDIRECT.format(LOG_FILE))
		#self.process.sendline(SRC_LINE)
		#self.process.expect(GDB_PROMPT)

		#self.process.sendline("continue")
		#self.process.expect(GDB_PROMPT)

		#line_num = parseLineNum()

		# TODO: Set up initial stack
		[frame, line] = self.gdbMainSetup()
		return [frame, line]

		#return line_num

	def gdbMainSetup(self):
		self.process.sendline(SRC_LINE)
		self.process.expect(GDB_PROMPT)

		self.flushToLogFile()
		line = parseLineNum()
		self.resetLogging()

		self.process.sendline(PRINT_REGISTER.format(BASE_POINTER))
		self.process.expect(GDB_PROMPT)

		self.flushToLogFile()
		[my_ebp] = parseRegisterVals()
		self.resetLogging()

		frame = StackFrame("main", my_ebp, None, None)

		self.process.sendline(INFO_ARGS)
		self.process.expect(GDB_PROMPT)

		self.flushToLogFile()
		locals_list = parseLocalsList()
		self.resetLogging()

		self.process.sendline(INFO_SCOPE.format(frame.title))
		self.process.expect(GDB_PROMPT)

		self.flushToLogFile()
		symbols = parseSymbols()
		self.resetLogging()

		for sym in symbols:
			item = FrameItem(sym.title, hex(int(frame.frame_ptr, 16) + int(sym.addr)), sym.length, None)
			frame.addItem(item)

			self.process.sendline(PRINT_SYMBOL.format(sym.title))
			self.process.expect(GDB_PROMPT)

		self.flushToLogFile()
		sym_vals = parseSymbolVals()
		self.resetLogging()

		assert(len(symbols) == len(sym_vals))

		for i in range(0, len(symbols)):
			item = frame.items[len(symbols) - 1 - i]
			# Locals are intitally null
			if item.title in locals_list:
				item.value = UNINITIALIZED
			else:
				item.value = sym_vals[i]

		return [frame, line]

		# TODO: Check if finished

	def gdbLineStep(self):
		self.resetLogging()

		self.process.sendline(LINE_STEP)
		self.process.expect(GDB_PROMPT)
		# Update stack args - check if hits breakpoint
		# If hits breakpoint, in new function - update stack
		# Check if finished

	def gdbFunctionStep(self):
		if not self.started:
			self.process.sendline(CONTINUE)
			self.process.expect(GDB_PROMPT)
		else:
			self.process.sendline(FUNCTION_STEP)
			self.process.expect(GDB_PROMPT)

		self.resetLogging()

		return self.gdbFunctionSetup()

		# TODO: Check if finished

	def gdbFunctionSetup(self):
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

		self.process.sendline(INFO_ARGS)
		self.process.expect(GDB_PROMPT)

		self.flushToLogFile()
		locals_list = parseLocalsList()
		self.resetLogging()

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
			item = FrameItem(sym.title, hex(int(frame.frame_ptr, 16) + int(sym.addr)), sym.length, None)
			frame.addItem(item)

			self.process.sendline(PRINT_SYMBOL.format(sym.title))
			self.process.expect(GDB_PROMPT)

		self.flushToLogFile()
		sym_vals = parseSymbolVals()
		self.resetLogging()

		assert(len(symbols) == len(sym_vals))

		for i in range(0, len(symbols)):
			item = frame.items[len(symbols) - 1 - i]
			# Locals are intitally null
			if item.title in locals_list:
				item.value = UNINITIALIZED
			else:
				item.value = sym_vals[i]

		return [frame, line]

		# TODO: Check if finished

	def gdbCheckForReturn():
		output = self.process.before.strip()

		# Returned with value
		retval_match = re.search(RETURN_REGEX, output)
		if retval_match:
			return [True, retval_match.group(1)]

		# Returned with no value
		retval_match = re_search(BREAKPOINT_REGEX, output)
		if retval_match:
			return [True, None]	

		return [False, None]

	def gdbRun(self):
		self.resetLogging()

		self.process.sendline(REMOVE_BR)
		self.process.expect(GDB_PROMPT)
		self.process.sendline(CONTINUE)
		self.process.expect(GDB_PROMPT)
		# Get result from log

	def gdbReset(self):
		if self.process:
			self.process.close()
			self.process = None
		# Clear stack
