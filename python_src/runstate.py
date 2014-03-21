import pexpect
from defs import *
from parse import *
from stackframe import *

# What if program needs user input?

class GDBProcess:

	def __init__(self):
		self.process = None
		self.started = False

	def gdbInit(self):
		# Open child bash process
		self.process = pexpect.spawn('bash')
		self.process.expect(BASH_PROMPT)
		self.process.sendline(GDB_INIT_CMD.format(INIT_FILE, C_OUT))
		self.process.expect(GDB_PROMPT)

		self.process.sendline(RUN)
		self.process.expect(GDB_PROMPT)
		assembly = parseAssembly(self.process.before.strip())

		[frame, line] = self.mainSetup()

		return [frame, line, assembly]

	def gdbLineStep(self):
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

		# Check if finished
		assembly = parseAssembly(self.process.before.strip())
		[frame, line] = self.functionSetup()
		return [frame, line, assembly]

	def gdbRun(self):
		self.process.sendline(REMOVE_BR)
		self.process.expect(GDB_PROMPT)
		self.process.sendline(CONTINUE)
		self.process.expect(GDB_PROMPT)
		# Get result

	def gdbReset(self):
		if self.process:
			self.process.close()
			self.process = None

	def mainSetup(self):
		line = self.getLineNum()

		my_ebp = self.getRegisterAddress(BASE_POINTER)

		frame = StackFrame("main", my_ebp, None, None)

		locals_list = self.getLocalVars()

		self.addSymbols(frame, locals_list)

		return [frame, line]

	def functionSetup(self):
		[title, line, bottom, registers] = self.getFrameInfo()

		my_ebp = self.getRegisterAddress(BASE_POINTER)
		my_esp = self.getRegisterAddress(STACK_POINTER)

		frame = StackFrame(title, my_ebp, my_esp, bottom)

		locals_list = self.getLocalVars()

		self.addSavedRegisters(frame, registers)
		self.addSymbols(frame, locals_list)

		# TODO: Check if finished
		return [frame, line]

	def getLineNum(self):
		self.process.sendline(SRC_LINE)
		self.process.expect(GDB_PROMPT)
		return parseLineNum(self.process.before.strip())

	def getFrameInfo(self):
		self.process.sendline(INFO_FRAME)
		self.process.expect(GDB_PROMPT)
		return parseFrameInfo(self.process.before.strip())

	def getLocalVars(self):
		self.process.sendline(INFO_ARGS)
		self.process.expect(GDB_PROMPT)
		return parseLocalsList(self.process.before.strip())

	def getSymbol(self, sym):
		self.process.sendline(PRINT_SYMBOL.format(sym.title))
		self.process.expect(GDB_PROMPT)
		return parseSymbolVal(self.process.before.strip())

	def getRegisterAddress(self, register_name):
		self.process.sendline(PRINT_REGISTER.format(register_name))
		self.process.expect(GDB_PROMPT)
		return parseRegisterVal(self.process.before.strip())

	def getRegisterVal(self, register_addr):
		self.process.sendline(VAL_AT_ADDR.format(1, register_addr))
		self.process.expect(GDB_PROMPT)
		return parseVal(self.process.before.strip())

	def addSymbols(self, frame, locals_list):
		self.process.sendline(INFO_SCOPE.format(frame.title))
		self.process.expect(GDB_PROMPT)
		symbols = parseSymbols(self.process.before.strip())

		for sym in symbols:
			if sym.title in locals_list:
				sym_val = UNINITIALIZED
			else:
				sym_val = self.getSymbol(sym)

			frame.addItem(FrameItem(sym.title, hex(int(frame.frame_ptr, 16) + int(sym.addr, 16)), sym.length, sym_val))

	def addSavedRegisters(self, frame, registers):
		for reg in registers:
			reg_val = self.getRegisterVal(reg.addr)

			if reg.title in BASE_POINTERS:
				reg.title = CALLEE_SAVED + " " + reg.title
			elif reg.title in STACK_POINTERS:
				reg.title = RETURN_ADDRESS
			
			frame.addItem(FrameItem(reg.title, reg.addr, reg.length, reg_val))

	def checkForReturn():
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
