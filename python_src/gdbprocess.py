import pexpect

from gdbdefs import *
from parse import *
from stackframe import *

class GDBProcess:
	""" Open gdb process for maintaining state of program execution """

	def __init__(self):
		self.process = None
		self.architecture = None
		self.started = False # Whether program has started execution
		self.finished = False # Whether program has exited
		self.mainBreakpoint = -1
		self.empty_frame = StackFrame(None, None, None, None, None, None, None)

	def gdbInit(self):
		""" Start new gdb process """
		self.started = False
		self.finished = False
		return self.startProcess()

	def gdbLineStep(self):
		""" Advance one source line """
		self.process.sendline(LINE_STEP)
		self.process.expect(GDB_PROMPT)
		return parseLineStepCheck(self.process.before.strip())

	def gdbFunctionStep(self):
		""" Advance one function call """
		if not self.started:
			# First function call out of main
			self.started = True
			self.process.sendline(CONTINUE)
			self.process.expect(GDB_PROMPT)
		else:
			self.process.sendline(FUNCTION_STEP)
			self.process.expect(GDB_PROMPT)

			if parseFunctionStepInMainCheck(self.process.before.strip()):
				# In main - "finish" command not valid so run "continue"
				self.process.sendline(CONTINUE)
				self.process.expect(GDB_PROMPT)
				if self.hitFinalBreakpoint(parseHitBreakpointNum(self.process.before.strip())):
					# Hit breakpoint at main exit
					return [self.empty_frame, None]
			else:
				[returned, val] = parseFunctionStepReturnCheck(self.process.before.strip())

				if returned:
					# Returned from function call with (possibly void) val
					return [None, val]

		# Stepped into new function
		return [self.functionSetup(), None]

	def gdbRun(self):
		""" Run program to completion """
		# Remove all breakpoints
		self.process.sendline(REMOVE_BR)
		self.process.expect(GDB_PROMPT)

		# Reset main breakpoint
		self.setMainBreakpoint()

		# Run program to end
		self.process.sendline(CONTINUE)
		self.process.expect(GDB_PROMPT)

	def gdbReset(self):
		""" Close gdb process """
		if self.process:
			self.process.close()
			self.process = None
			self.finished = False

	def gdbFinishUp(self):
		""" Run process through exit and return exit status """
		self.finished = True
		self.process.sendline(CONTINUE)
		self.process.expect(GDB_PROMPT)
		return parseExitStatus(self.process.before.strip())

	def gdbUpdateTopFrame(self, frame):
		""" Update uppermost frame on stack """
		[frame.line, frame.assembly] = self.getLineAndAssembly()
		frame.stack_pointer = self.getRegisterValue(self.architecture.stack_pointer)
		self.updateAllSymbols(frame)

		return frame

	def gdbUpdatePreviousFrame(self, frame):
		""" Update frame directly below top frame on stack """
		# Navigate one frame up
		self.process.sendline(LAST_FRAME)
		self.process.expect(GDB_PROMPT)

		self.gdbUpdateTopFrame(frame)

		# Return to top frame
		self.process.sendline(NEXT_FRAME)
		self.process.expect(GDB_PROMPT)

	def startProcess(self):
		""" Set up bash process and open gdb session with compiled program """
		self.process = pexpect.spawn('bash')
		self.process.expect(BASH_PROMPT)

		# Command file sets breakpoints at start of all functions
		self.process.sendline(GDB_INIT_CMD.format(GDB_INIT_SCRIPT, C_OUT))
		self.process.expect(GDB_PROMPT)

		# 32- or 64-bit x86
		self.setArchitecture()

		# Set breakpoint right before return from main to detect program completion
		self.setMainBreakpoint()

		# Run until enters main
		self.process.sendline(RUN)
		self.process.expect(GDB_PROMPT)

		return self.mainSetup()

	def mainSetup(self):
		""" Set up initial stack frame for main """
		[line, assembly] = self.getLineAndAssembly()

		base_pointer = self.getRegisterValue(self.architecture.base_pointer)

		# Main has no stack pointer or base address
		frame = StackFrame(MAIN, self.architecture, base_pointer, None, None, line, assembly)

		self.addAllSymbols(frame)

		return frame

	def functionSetup(self):
		""" Set up initial stack frame for non-main function """
		[line, assembly] = self.getLineAndAssembly()
		[title, bottom, registers] = self.getFrameInfo()

		base_pointer = self.getRegisterValue(self.architecture.base_pointer)
		stack_pointer = self.getRegisterValue(self.architecture.stack_pointer)

		frame = StackFrame(title, self.architecture, base_pointer, stack_pointer, bottom, line, assembly)

		self.addSavedRegisters(frame, registers)
		self.addAllSymbols(frame)

		return frame

	def setArchitecture(self):
		""" Set machine architecture for source file - only supports 32- and 64- bit x86 """
		self.process.sendline(INFO_TARGET)
		self.process.expect(GDB_PROMPT)

		# Note: does not check for unsupported architecture
		bits = parseArchitecture(self.process.before.strip())

		if bits:
			# Save as 32- or 64-bit for accessing registers
			self.architecture = MachineArchitecture(int(bits))	

	def setMainBreakpoint(self):
		""" Set breakpoint at return in main and return breakpoint number """
		self.process.sendline(DISAS_MAIN)

		while (True):
			# Check for <return to continue> prompt - send returns until command finishes
			i = self.process.expect([GDB_PROMPT, RETURN_TO_CONTINUE])
			if i == 1:
				self.process.sendline("")
			else:
				break

		# Get address of line right before main exit
		main_addr = parseMainReturnAddress(self.process.before.strip())

		# Set breakpoint right before main exit and save breakpoint number
		self.process.sendline(BREAK_ADDR.format(main_addr))
		self.process.expect(GDB_PROMPT)
		self.mainBreakpoint = parseSetBreakpointNum(self.process.before.strip())

	def returningFromMain(self, frame):
		""" Check if function about to exit from main """
		return frame == self.empty_frame

	def hitFinalBreakpoint(self, num):
		""" Check if hit final main breakpoint """
		return self.mainBreakpoint == num

	def setSymbolInfo(self, var, frame_item, frame_ptr):
		""" Set title, length, and address for symbol """
		frame_item.title = var

		self.process.sendline(SIZEOF.format(var))
		self.process.expect(GDB_PROMPT)
		frame_item.length = parseValue(self.process.before.strip())

		self.process.sendline(INFO_ADDRESS.format(var))
		self.process.expect(GDB_PROMPT)
		offset = parseAddress(self.process.before.strip())
		# Address is base pointer plus offset
		frame_item.addr = hex(int(frame_ptr, 16) + int(offset, 16))

	def setSymbolValue(self, var, frame_item):
		""" Set value and zoom value of symbol """
		full_val = self.getSymbolValue(var)
		[frame_item.struct, frame_item.value] = parseStructCheck(full_val)
		frame_item.initialized = True
		self.setZoomValue(frame_item)

	def setZoomValue(self, frame_item):
		""" Get zoom value of symbol """
		if frame_item.struct:
			# Symbol is a struct
			if int(frame_item.value, 16) == NULL_VAL or not frame_item.initialized:
				# If 0x0 struct or uninitialized, struct is null
				frame_item.zoom_val = UNINITIALIZED
			else:
				# Get info about struct members
				self.process.sendline(PRINT_POINTER.format(frame_item.title))
				self.process.expect(GDB_PROMPT)
				frame_item.zoom_val = parseValue(self.process.before.strip())
		else:
			# Zoom value of a non-struct is just its value
			frame_item.zoom_val = frame_item.value

	def addAllSymbols(self, frame):
		""" Get all symbols on initial function entry """
		for arg in self.getArgs():
			# Set up args
			frame_item = FrameItem()
			self.setSymbolInfo(arg, frame_item, frame.frame_ptr)
			self.setSymbolValue(arg, frame_item)
			frame.addItem(frame_item)

		for local in self.getLocalVars():
			# Set up local variables
			frame_item = FrameItem()
			self.setSymbolInfo(local, frame_item, frame.frame_ptr)
			full_val = self.getSymbolValue(local)
			[frame_item.struct, frame_item.value] = parseStructCheck(full_val)
			# Locals are uninitialized on function enter
			frame_item.initialized = False
			frame_item.zoom_val = UNINITIALIZED
			frame.addItem(frame_item)

	def updateAllSymbols(self, frame):
		""" Update values of all symbols in frame """
		for item in frame.items:
			# Don't update saved registers
			if CALLER_SAVED not in item.title and RETURN_ADDRESS not in item.title:
				self.updateSymbolValue(item)

	def updateSymbolValue(self, frame_item):
		""" Update value of symbol """
		full_val = self.getSymbolValue(frame_item.title)
		[struct, val] = parseStructCheck(full_val)

		if frame_item.value != val:
			# Value has changed so must be initialized
			frame_item.value = val
			frame_item.struct = struct
			frame_item.initialized = True

		self.setZoomValue(frame_item)

	def addSavedRegisters(self, frame, registers):
		""" Get values of saved registers on initial function entry """
		for reg in registers:
			frame_item = FrameItem()

			frame_item.addr = reg.addr
			frame_item.length = self.architecture.reg_length
			frame_item.initialized = True # saved registers are always initialized
			frame_item.value = self.getSavedRegisterValue(reg.title)
			frame_item.zoom_val = frame_item.value
			frame_item.struct = NON_STRUCT # registers are never structs

			if reg.title == self.architecture.base_pointer:
				# Set title for saved base pointer
				frame_item.title = CALLER_SAVED + " " + reg.title
			elif reg.title == self.architecture.instr_pointer:
				# Set title for return address
				frame_item.title = RETURN_ADDRESS
				base_addr = parseReturnAddress(frame_item.value)
				self.process.sendline(INSTR_AT_ADDR.format(base_addr))
				self.process.expect(GDB_PROMPT)
				# Zoom value of return address is corresponding assembly instruction
				frame_item.zoom_val = parseInstruction(self.process.before)
			
			frame.addItem(frame_item)

	def getFrameInfo(self):
		""" Get function title, base address, and saved registers """
		self.process.sendline(INFO_FRAME)
		self.process.expect(GDB_PROMPT)
		return parseFrameInfo(self.process.before.strip())

	def getLineAndAssembly(self):
		""" Get current source line number and corresponding assembly instructions """
		self.process.sendline(INFO_LINE)
		self.process.expect(GDB_PROMPT)
		[line, assembly_start, assembly_end] = parseLineAndAssembly(self.process.before.strip())
		
		# Increment end address by one so inclusive
		# Will otherwise be blank if returning from function with no immediate assignment
		self.process.sendline(DISAS.format(assembly_start, hex(int(assembly_end, 16)+1)))
		self.process.expect(GDB_PROMPT)
		assembly = parseAssembly(self.process.before.strip())
		return [line, assembly]

	def getArgs(self):
		""" Get function argument names """
		self.process.sendline(INFO_ARGS)
		self.process.expect(GDB_PROMPT)
		return parseVarList(self.process.before.strip())

	def getLocalVars(self):
		""" Get function local variable names """
		self.process.sendline(INFO_LOCALS)
		self.process.expect(GDB_PROMPT)
		return parseVarList(self.process.before.strip())

	def getSymbolValue(self, var):
		""" Get value of symbol """
		self.process.sendline(PRINT_VAR.format(var))
		self.process.expect(GDB_PROMPT)
		return parseValue(self.process.before.strip())

	def getRegisterValue(self, register_name):
		""" Get value of register """
		self.process.sendline(PRINT_REGISTER.format(register_name))
		self.process.expect(GDB_PROMPT)
		return parseRegisterValue(self.process.before.strip())

	def getSavedRegisterValue(self, register_name):
		""" Get value of saved register from previous frame """
		# Navigate one frame up
		self.process.sendline(LAST_FRAME)
		self.process.expect(GDB_PROMPT)

		self.process.sendline(PRINT_REGISTER.format(register_name))
		self.process.expect(GDB_PROMPT)
		val = parseSavedRegisterValue(self.process.before.strip())

		# Return to top frame
		self.process.sendline(NEXT_FRAME)
		self.process.expect(GDB_PROMPT)

		return val
