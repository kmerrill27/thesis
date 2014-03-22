import pexpect
from defs import *
from parse import *
from arch import *
from stackframe import *

# What if program needs user input?

class GDBProcess:

	def __init__(self):
		self.process = None
		self.architecture = None
		self.started = False

	def gdbInit(self):
		# Open child bash process
		self.started = False
		self.process = pexpect.spawn('bash')
		self.process.expect(BASH_PROMPT)
		self.process.sendline(GDB_INIT_CMD.format(INIT_FILE, C_OUT))
		self.process.expect(GDB_PROMPT)

		# TODO: check if unsupported architecture
		self.setArchitecture()

		self.process.sendline(RUN)
		self.process.expect(GDB_PROMPT)

		return self.mainSetup(self.process.before.strip())

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

		# Check if returned
		#[returned, retval] = parseReturnCheck(self.process.before.strip())
		return self.functionSetup(self.process.before.strip())

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

	def gdbUpdateFrame(self, frame):
		self.process.sendline(LAST_FRAME)
		self.process.expect(GDB_PROMPT)

		[line, assembly] = self.getLineAndAssembly()

		my_esp = self.getRegisterAddress(self.architecture.stack_pointer)

		self.process.sendline(INFO_LOCALS)
		self.process.expect(GDB_PROMPT)
		locals_list = parseLocalsList(self.process.before.strip())

		# Update values of local variables
		for item in frame.items:
			for local in locals_list:
				if item.title == local.title and item.value != local.value:
					item.value = local.value
					if not item.initialized:
						item.initialized = True

		frame.line = line
		frame.assembly = assembly
		frame.stack_pointer = my_esp

		self.process.sendline(NEXT_FRAME)
		self.process.expect(GDB_PROMPT)

	def mainSetup(self, output):
		assembly = parseAssembly(output)

		line = self.getLineNum()

		my_ebp = self.getRegisterAddress(self.architecture.base_pointer)

		frame = StackFrame("main", self.architecture, my_ebp, None, None, line, assembly)

		locals_list = self.getLocalVars()

		self.addSymbols(frame, locals_list)

		return frame

	def functionSetup(self, output):
		assembly = parseAssembly(output)

		[title, line, bottom, registers] = self.getFrameInfo()

		my_ebp = self.getRegisterAddress(self.architecture.base_pointer)
		my_esp = self.getRegisterAddress(self.architecture.stack_pointer)

		frame = StackFrame(title, self.architecture, my_ebp, my_esp, bottom, line, assembly)

		locals_list = self.getLocalVars()

		self.addSavedRegisters(frame, registers)
		self.addSymbols(frame, locals_list)

		# TODO: Check if finished
		return frame

	def setArchitecture(self):
		self.process.sendline(INFO_TARGET)
		self.process.expect(GDB_PROMPT)
		bits = parseArchitecture(self.process.before.strip())

		self.architecture = MachineArchitecture()
		self.architecture.setArchitecture(int(bits))

	def getLineAndAssembly(self):
		self.process.sendline(SRC_LINE)
		self.process.expect(GDB_PROMPT)
		[line, assembly_start, assembly_end] = parseLineAndAssembly(self.process.before.strip())
		self.process.sendline(DISAS.format(assembly_start, assembly_end))
		self.process.expect(GDB_PROMPT)
		assembly = parseAssembly(self.process.before.strip())
		return [line, assembly]

	def getLineNum(self):
		self.process.sendline(SRC_LINE)
		self.process.expect(GDB_PROMPT)
		return parseLineNum(self.process.before.strip())

	def getFrameInfo(self):
		self.process.sendline(INFO_FRAME)
		self.process.expect(GDB_PROMPT)
		return parseFrameInfo(self.process.before.strip(), self.architecture.reg_length)

	def getLocalVars(self):
		self.process.sendline(INFO_LOCALS)
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

	def getSavedRegisterVal(self, register_name):
		self.process.sendline(LAST_FRAME)
		self.process.expect(GDB_PROMPT)

		self.process.sendline(PRINT_REGISTER.format(register_name))
		self.process.expect(GDB_PROMPT)
		val = parseSavedRegisterVal(self.process.before.strip())

		self.process.sendline(NEXT_FRAME)
		self.process.expect(GDB_PROMPT)
		return val

	def addSymbols(self, frame, locals_list):
		self.process.sendline(INFO_SCOPE.format(frame.title))
		self.process.expect(GDB_PROMPT)
		symbols = parseSymbols(self.process.before.strip())

		for sym in symbols:
			initialized = True
			for local in locals_list:
				if sym.title == local.title:
					initialized = False
			
			sym_val = self.getSymbol(sym)

			frame.addItem(FrameItem(sym.title, hex(int(frame.frame_ptr, 16) + int(sym.addr, 16)), sym.length, sym_val, initialized))

	def addSavedRegisters(self, frame, registers):
		for reg in registers:
			reg_val = self.getSavedRegisterVal(reg.title)

			if reg.title == self.architecture.base_pointer:
				reg.title = CALLEE_SAVED + " " + reg.title
			elif reg.title == self.architecture.instr_pointer:
				reg.title = RETURN_ADDRESS
			
			frame.addItem(FrameItem(reg.title, reg.addr, reg.length, reg_val, True))
