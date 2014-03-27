import pexpect

from arch import *
from defs import *
from parse import *
from stackframe import *

class GDBProcess:
	""" Open gdb process for maintaining state of program execution """

	def __init__(self):
		self.process = None
		self.architecture = None
		self.started = False
		self.mainBreakpoint = -1
		self.empty_frame = StackFrame(None, None, None, None, None, None, None)

	def gdbInit(self):
		self.started = False
		# Open bash process
		return self.startProcess()

	def setMainBreakpoint(self):
		self.process.sendline(DISAS_MAIN)

		while (True):
			# Check for <return to continue> prompt - send returns until command finishes
			i = self.process.expect([GDB_PROMPT, RETURN_TO_CONTINUE])
			if i == 1:
				self.process.sendline("")
			else:
				break

		# Get address of line right before main exit
		pop_addr = parsePopAddress(self.process.before.strip())

		# Set breakpoint right before main exit and save breakpoint number
		self.process.sendline(BREAK_ADDR.format(pop_addr))
		self.process.expect(GDB_PROMPT)
		self.mainBreakpoint = parseSetBreakpointNum(self.process.before.strip())

	def gdbFinishUp(self):
		# Run process through exit and return exit status
		self.process.sendline(CONTINUE)
		self.process.expect(GDB_PROMPT)
		return parseExitCode(self.process.before.strip())

	def gdbLineStep(self):
		# Advance one source line
		self.process.sendline(LINE_STEP)
		self.process.expect(GDB_PROMPT)
		return parseLineStepCheck(self.process.before.strip())

	def gdbFunctionStep(self):
		# Advance one function call
		if not self.started:
			# First function call out of main
			self.started = True
			self.process.sendline(CONTINUE)
			self.process.expect(GDB_PROMPT)
		else:
			self.process.sendline(FUNCTION_STEP)
			self.process.expect(GDB_PROMPT)

			if parseInMainCheck(self.process.before.strip()):
				# In main - "finish" command not valid so run "continue"
				self.process.sendline(CONTINUE)
				self.process.expect(GDB_PROMPT)
				if self.hitFinalBreakpoint(parseHitBreakpointNum(self.process.before.strip())):
					# Hit breakpoint at main exit
					return [self.empty_frame, None]
			else:
				[returned, val] = parseReturnCheck(self.process.before.strip())

				if returned:
					# Returned from function call with (possibly void) val
					return [None, val]

		# Stepped into new function
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

	def returningFromMain(self, frame):
		return frame == self.empty_frame

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
		# Set up bash process and open gdb session with compiled program
		self.process = pexpect.spawn('bash')
		self.process.expect(BASH_PROMPT)

		# Command file sets breakpoints at start of all functions
		self.process.sendline(GDB_INIT_CMD.format(INIT_FILE, C_OUT))
		self.process.expect(GDB_PROMPT)

		# 32- or 64-bit x86
		self.setArchitecture()

		# Set breakpoint right before return from main to detect program completion
		self.setMainBreakpoint()

		# Run until enters main
		self.process.sendline(RUN)
		self.process.expect(GDB_PROMPT)

		return self.mainSetup()

	def setArchitecture(self):
		self.process.sendline(INFO_TARGET)
		self.process.expect(GDB_PROMPT)

		# Only supports 32- and 64-bit x86 architecture
		bits = parseArchitecture(self.process.before.strip())

		if bits:
			# Save as 32- or 64-bit for accessing registers
			self.architecture = MachineArchitecture()
			self.architecture.setArchitecture(int(bits))

	def hitFinalBreakpoint(self, num):
		return self.mainBreakpoint == num

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

	def getNumFrames(self):
		self.process.sendline(INFO_STACK)
		self.expect(GDB_PROMPT)
		return parseNumFrames(self.process.before.strip())

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

	def getSymbolValue(self, var):
		self.process.sendline(PRINT_VAR.format(var))
		self.process.expect(GDB_PROMPT)
		return parseValue(self.process.before.strip())

	def setZoomValue(self, frame_item):
		if frame_item.struct:
			if int(frame_item.value, 16) == NULL_VAL or not frame_item.initialized:
				frame_item.zoom_val = UNINITIALIZED
			else:
				self.process.sendline(PRINT_POINTER.format(frame_item.title))
				self.process.expect(GDB_PROMPT)
				frame_item.zoom_val = parseValue(self.process.before.strip())
		else:
			frame_item.zoom_val = frame_item.value

	def setSymbolValue(self, var, frame_item):
		full_val = self.getSymbolValue(var)
		[frame_item.struct, frame_item.value] = parseStructCheck(full_val)
		frame_item.initialized = True
		self.setZoomValue(frame_item)

	def updateSymbolValue(self, frame_item):
		full_val = self.getSymbolValue(frame_item.title)
		[struct, val] = parseStructCheck(full_val)

		if frame_item.value != val:
			frame_item.value = val
			frame_item.struct = struct
			frame_item.initialized = True

		self.setZoomValue(frame_item)

	def addAllSymbols(self, frame):
		for arg in self.getArgs():
			frame_item = FrameItem()
			self.setSymbolInfo(arg, frame_item, frame.frame_ptr)
			self.setSymbolValue(arg, frame_item)
			frame.addItem(frame_item)

		for local in self.getLocalVars():
			frame_item = FrameItem()
			self.setSymbolInfo(local, frame_item, frame.frame_ptr)
			full_val = self.getSymbolValue(local)
			[frame_item.struct, frame_item.value] = parseStructCheck(full_val)
			# Locals are uninitialized on function enter
			frame_item.initialized = False
			frame_item.zoom_val = UNINITIALIZED
			frame.addItem(frame_item)

	def updateAllSymbols(self, frame):
		for item in frame.items:
			# Don't update saved registers
			if CALLER_SAVED not in item.title and RETURN_ADDRESS not in item.title:
				self.updateSymbolValue(item)

	def addSavedRegisters(self, frame, registers):
		for reg in registers:
			frame_item = FrameItem()

			frame_item.addr = reg.addr
			frame_item.length = reg.length
			frame_item.initialized = True
			frame_item.value = self.getSavedRegisterVal(reg.title)
			frame_item.zoom_val = frame_item.value
			frame_item.struct = NON_STRUCT

			if reg.title == self.architecture.base_pointer:
				frame_item.title = CALLER_SAVED + " " + reg.title
			elif reg.title == self.architecture.instr_pointer:
				frame_item.title = RETURN_ADDRESS
			
			frame.addItem(frame_item)
