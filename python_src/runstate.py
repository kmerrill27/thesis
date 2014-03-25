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
		self.mainBreakpoint = -1
		self.empty_frame = StackFrame(None, None, None, None, None, None, None)

	def gdbInit(self):
		# Open child bash process
		self.started = False
		return self.startProcess()

	def setMainBreakpoint(self):
		self.process.sendline(DISAS_MAIN)
		while (True):
			i = self.process.expect([GDB_PROMPT, RETURN_TO_CONTINUE])
			if i == 1:
				self.process.sendline("")
			else:
				break

		# Get address of right before main exit
		pop_addr = parsePopAddress(self.process.before.strip())

		self.process.sendline(BREAK_ADDR.format(pop_addr))
		self.process.expect(GDB_PROMPT)
		self.mainBreakpoint = parseSetBreakpointNum(self.process.before.strip())

	def gdbFinishUp(self):
		self.process.sendline(CONTINUE)
		self.process.expect(GDB_PROMPT)
		return parseExitCode(self.process.before.strip())

	def gdbLineStep(self):
		self.process.sendline(LINE_STEP)
		self.process.expect(GDB_PROMPT)
		# Update stack args - check if hits breakpoint
		# If hits breakpoint, in new function - update stack
		# Check if finished

	def gdbFunctionStep(self):
		if not self.started:
			self.started = True
			self.process.sendline(CONTINUE)
			self.process.expect(GDB_PROMPT)
		else:
			self.process.sendline(FUNCTION_STEP)
			self.process.expect(GDB_PROMPT)

			if parseInMainCheck(self.process.before.strip()):
				self.process.sendline(CONTINUE)
				self.process.expect(GDB_PROMPT)
				if self.mainBreakpoint == parseHitBreakpointNum(self.process.before.strip()):
					return [self.empty_frame, None]
			else:
				[returned, val] = parseReturnCheck(self.process.before.strip())

				if returned:
					return [None, val]

		return [self.functionSetup(), None]

	def gdbRun(self):
		self.process.sendline(REMOVE_BR)
		self.process.expect(GDB_PROMPT)
		self.setMainBreakpoint()
		self.process.sendline(CONTINUE)
		self.process.expect(GDB_PROMPT)

	def gdbReset(self):
		if self.process:
			self.process.close()
			self.process = None

	def gdbUpdateCurrentFrame(self, frame):
		[frame.line, frame.assembly] = self.getLineAndAssembly()
		frame.stack_pointer = self.getRegisterAddress(self.architecture.stack_pointer)
		self.updateAllSymbols(frame)

		return frame

	def gdbUpdateFrame(self, frame):
		self.process.sendline(LAST_FRAME)
		self.process.expect(GDB_PROMPT)

		self.gdbUpdateCurrentFrame(frame)

		self.process.sendline(NEXT_FRAME)
		self.process.expect(GDB_PROMPT)

	def mainSetup(self):
		[line, assembly] = self.getLineAndAssembly()

		my_ebp = self.getRegisterAddress(self.architecture.base_pointer)

		frame = StackFrame("main", self.architecture, my_ebp, None, None, line, assembly)

		self.addAllSymbols(frame)

		return frame

	def functionSetup(self):
		[line, assembly] = self.getLineAndAssembly()
		[title, bottom, registers] = self.getFrameInfo()

		my_ebp = self.getRegisterAddress(self.architecture.base_pointer)
		my_esp = self.getRegisterAddress(self.architecture.stack_pointer)

		frame = StackFrame(title, self.architecture, my_ebp, my_esp, bottom, line, assembly)

		self.addSavedRegisters(frame, registers)
		self.addAllSymbols(frame)

		return frame

	def startProcess(self):
		self.process = pexpect.spawn('bash')
		self.process.expect(BASH_PROMPT)
		self.process.sendline(GDB_INIT_CMD.format(INIT_FILE, C_OUT))
		self.process.expect(GDB_PROMPT)

		# TODO: check if unsupported architecture
		self.setArchitecture()
		self.setMainBreakpoint()

		self.process.sendline(RUN)
		self.process.expect(GDB_PROMPT)

		return self.mainSetup()

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
		
		# Add one to address so inclusive of add instruction
		self.process.sendline(DISAS.format(assembly_start, hex(int(assembly_end, 16)+1)))
		self.process.expect(GDB_PROMPT)
		assembly = parseAssembly(self.process.before.strip())
		return [line, assembly]

	def getFrameInfo(self):
		self.process.sendline(INFO_FRAME)
		self.process.expect(GDB_PROMPT)
		return parseFrameInfo(self.process.before.strip(), self.architecture.reg_length)

	def getArgs(self):
		self.process.sendline(INFO_ARGS)
		self.process.expect(GDB_PROMPT)
		return parseVarList(self.process.before.strip())

	def getLocalVars(self):
		self.process.sendline(INFO_LOCALS)
		self.process.expect(GDB_PROMPT)
		return parseVarList(self.process.before.strip())

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

	def setSymbolInfo(self, var, frame_item, frame_ptr):
		frame_item.title = var

		self.process.sendline(SIZEOF.format(var))
		self.process.expect(GDB_PROMPT)
		frame_item.length = parseValue(self.process.before.strip())

		self.process.sendline(INFO_ADDRESS.format(var))
		self.process.expect(GDB_PROMPT)
		addr = parseAddress(self.process.before.strip())
		frame_item.addr = hex(int(frame_ptr, 16) + int(addr, 16))
		frame_item.struct = parseStructCheck(self.process.before.strip())

	def getSymbolValue(self, var):
		self.process.sendline(PRINT_VAR.format(var))
		self.process.expect(GDB_PROMPT)
		return parseValue(self.process.before.strip())

	def getStructZoomValue(self, frame_item):
		if frame_item.struct:
			if int(val, 16) == NULL_VAL or not frame_item.initialized:
				frame.zoom_val = "null"
			else:
				self.process.sendline(PRINT_POINTER.format(frame_item.title))
				self.process.expect(GDB_PROMPT)
				frame_item.zoom_val = parseValue(self.process.before.strip())

	def setSymbolValue(self, var, frame_item):
		frame_item.value = self.getSymbolValue(var)
		frame_item.initialized = True
		self.getStructZoomValue(frame_item)

	def updateSymbolValue(self, frame_item):
		val = self.getSymbolValue(frame_item.title)

		if frame_item.value != val:
			frame_item.value = val
			frame_item.initialized = True

		self.getStructZoomValue(frame_item)

	def addAllSymbols(self, frame):
		for arg in self.getArgs():
			frame_item = FrameItem()
			self.setSymbolInfo(arg, frame_item, frame.frame_ptr)
			self.setSymbolValue(arg, frame_item)
			frame.addItem(frame_item)

		for local in self.getLocalVars():
			frame_item = FrameItem()
			self.setSymbolInfo(local, frame_item, frame.frame_ptr)
			# Locals are uninitialized on function enter
			frame_item.value = self.getSymbolValue(local)
			frame_item.initialized = False
			frame_item.zoom_val = UNINITIALIZED
			frame.addItem(frame_item)

	def updateAllSymbols(self, frame):
		for item in frame.items:
			# Don't update saved registers
			if CALLEE_SAVED not in item.title and RETURN_ADDRESS not in item.title:
				self.updateSymbolValue(item)

	def addSavedRegisters(self, frame, registers):
		for reg in registers:
			frame_item = FrameItem()

			frame_item.addr = reg.addr
			frame_item.length = reg.length
			frame_item.initialized = True
			frame_item.value = self.getSavedRegisterVal(reg.title)
			frame_item.zoom_val = frame_item.value

			if reg.title == self.architecture.base_pointer:
				frame_item.title = CALLEE_SAVED + " " + reg.title
			elif reg.title == self.architecture.instr_pointer:
				frame_item.title = RETURN_ADDRESS
			
			frame.addItem(frame_item)
