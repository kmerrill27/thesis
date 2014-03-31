import pexpect

from gdbdefs import *
from parse import *
from stackframe import *

class Breakpoint:
	""" Representation of a set breakpoint """

	def __init__(self, num, break_start, break_end):
		self.num = num # breakpoint number
		self.break_start = break_start # first assembly instr address of break line
		self.break_end = break_end # last assembly instr address of break line

class GDBProcess:
	""" Open gdb process for maintaining state of program execution """

	def __init__(self):
		self.process = None
		self.architecture = None
		self.started = False # Whether program has started execution
		self.finished = False # Whether program has exited
		self.return_breakpoints = {}
		self.current_function = None

	def gdbInit(self):
		""" Start new gdb process """
		self.started = False
		self.finished = False
		return self.startProcess()

	def gdbLineStep(self, frame):
		""" Advance one source line """
		self.process.sendline(LINE_STEP)
		self.process.expect(GDB_PROMPT)

		my_break = self.return_breakpoints[self.current_function]
		break_num = parseHitBreakpointNum(self.process.before.strip())

		if not break_num:
			self.process.sendline(CURRENT_INSTRUCTION)
			self.process.expect(GDB_PROMPT)
			addr = parseAssemblyAddress(self.process.before.strip())

			if self.current_function != MAIN and addr >= my_break.break_start and addr <= my_break.break_end:
				# Returned sneakily - returned back into middle of line with return breakpoint
				return self.functionReturnSetup(None)
			else:
				# Inside same function
				return [self.gdbUpdateTopFrame(frame), None, False]
		elif break_num == my_break.num:
			# Returned from function
			return self.functionReturnSetup(break_num)

		# Stepped into new function
		return [self.functionSetup(), break_num, False]

	def gdbFunctionStep(self):
		""" Advance one function call """
		self.process.sendline(CONTINUE)
		self.process.expect(GDB_PROMPT)

		my_break = self.return_breakpoints[self.current_function]
		break_num = parseHitBreakpointNum(self.process.before.strip())
		if break_num == my_break.num:
			# Returned from function
			return self.functionReturnSetup(break_num)

		# Stepped into new function
		return [self.functionSetup(), None, False]	

	def gdbRun(self):
		""" Run program to completion """
		# Disable all breakpoints
		self.process.sendline(DISABLE_ALL_BREAKPOINTS)
		self.process.expect(GDB_PROMPT)

		# Re-enable main return breakpoint
		self.process.sendline(ENABLE_BREAKPOINT.format(self.return_breakpoints[MAIN].num))
		self.process.expect(GDB_PROMPT)

		# Run program to end
		self.process.sendline(CONTINUE)
		self.process.expect(GDB_PROMPT)

	def gdbReset(self):
		""" Close gdb process """
		if self.process:
			self.process.close()
			self.process = None
			self.current_function = None
			self.return_breakpoints = {}
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
		
		# Don't add stack pointer to main frame
		if frame.stack_ptr:
			frame.stack_ptr = self.getRegisterValue(self.architecture.stack_pointer)

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

	def setCurrentFunction(self, name):
		self.current_function = name

	def startProcess(self):
		""" Set up bash process and open gdb session with compiled program """
		self.started = True
		self.process = pexpect.spawn('bash')
		self.process.expect(BASH_PROMPT)

		# Command file sets breakpoints at start of all functions
		self.process.sendline(GDB_INIT_CMD.format(GDB_INIT_SCRIPT, C_OUT))
		self.process.expect(GDB_PROMPT)

		# 32- or 64-bit x86
		self.setArchitecture()

		# Set and disable breakpoints at function returns
		# Main return breakpoint left enabled
		self.setReturnBreakpoints()

		# Run until enters main
		self.process.sendline(RUN)
		self.process.expect(GDB_PROMPT)

		return self.mainSetup()

	def setReturnBreakpoints(self):
		""" Set breakpoints right before exit of all functions """
		# Get all function names in source file
		self.process.sendline(INFO_FUNCTIONS)
		self.process.expect(GDB_PROMPT)
		functions = parseFunctionNames(self.process.before.strip())

		for function in functions:
			self.process.sendline(DISAS_FUNCTION.format(function))

			# Get address of line right before function exit
			addr = parseReturnInstrAddress(self.returnToContinue())

			# Set breakpoint right before function exit and save breakpoint number
			self.process.sendline(BREAK_AT_ADDRESS.format(addr))
			self.process.expect(GDB_PROMPT)
			num = parseSetBreakpointNum(self.process.before.strip())

			# Get line number of exit address
			# Breakpoint must be at line, not address to avoid double return
			self.process.sendline(LINE_AT_ADDR.format(addr))
			self.process.expect(GDB_PROMPT)
			[line, start_addr, end_addr] = parseLineAndAssembly(self.process.before.strip())

			self.return_breakpoints[function] = Breakpoint(num, start_addr, end_addr)

	def mainSetup(self):
		""" Set up initial stack frame for main """
		[line, assembly] = self.getLineAndAssembly()

		base_pointer = self.getRegisterValue(self.architecture.base_pointer)

		# Main has no stack pointer or base address
		frame = StackFrame(MAIN, self.architecture, base_pointer, None, None, line, assembly)

		self.addAllSymbols(frame)

		self.current_function = MAIN

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

		self.current_function = title

		return frame

	def functionReturnSetup(self, break_num):
		""" Set up process returning from a function """
		if self.return_breakpoints[MAIN].num == break_num:
			# Hit breakpoint at main exit
			return [None, None, True]

		# Hit breakpoint at function exit - finish up function
		self.process.sendline(FUNCTION_STEP)
		self.process.expect(GDB_PROMPT)

		if not break_num:
			# Run it again because hit exit breakpoint on last 'finish'
			self.process.sendline(FUNCTION_STEP)
			self.process.expect(GDB_PROMPT)

		return [None, parseFunctionStepReturnValue(self.process.before.strip()), False]

	def returnToContinue(self):
		""" Click through <return to continue> prompts until complete """
		last_page = ""
		while (True):
			# Check for <return to continue> prompt - send returns until command finishes
			i = self.process.expect([GDB_PROMPT, RETURN_TO_CONTINUE])
			if i == 1:
				# Save last lines in case pop and retq instructions straddle prompt
				last_page = self.process.before.strip()
				self.process.sendline(CARRIAGE_RETURN)
			else:
				break
		return last_page + "\n" + self.process.before.strip()

	def setArchitecture(self):
		""" Set machine architecture for source file - only supports 32- and 64- bit x86 """
		self.process.sendline(INFO_TARGET)
		self.process.expect(GDB_PROMPT)

		# Note: does not check for unsupported architecture
		bits = parseArchitecture(self.process.before.strip())

		if bits:
			# Save as 32- or 64-bit for accessing registers
			self.architecture = MachineArchitecture(int(bits))

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
		frame_item.addr = hex(int(frame_ptr, 16) + int(offset))

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
		self.process.sendline(DISAS_LINE.format(assembly_start, hex(int(assembly_end, 16)+1)))
		assembly = parseAssembly(self.returnToContinue())

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
