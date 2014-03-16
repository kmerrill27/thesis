import pexpect
from defs import *

def gdb_init():
	# Open child bash process
	gdb_process = pexpect.spawn('bash')
	gdb_process.expect(BASH_PROMPT)
	gdb_process.sendline(GDB_INIT_CMD.format(INIT_FILE, C_OUT))
	gdb_process.expect(GDB_PROMPT)

	# Set up logging to file
	gdb_process.sendline(SET_LOG_FILE.format(LOG_FILE))
	gdb_process.expect(GDB_PROMPT)
	gdb_process.sendline(SET_LOG_ON)
	gdb_process.expect(GDB_PROMPT)
	gdb_process.sendline(RUN)
	gdb_process.expect(GDB_PROMPT)
	# Set up initial stack

def gdb_line_step():
	gdb_process.sendline(LINE_STEP)
	gdb_process.expect(GDB_PROMPT)
	# Update stack args - check if hits breakpoint
	# If hits breakpoint, in new function - update stack

def gdb_function_step():
	gdb_process.sendline(FUNCTION_STEP)
	gdb_process.expect(GDB_PROMPT)
	# Update stack

def gdb_run():
	gdb_process.sendline(REMOVE_BR)
	gdb_process.expect(GDB_PROMPT)
	gdb_process.sendline(RUN)
	gdb_process.expect(GDB_PROMPT)
	# Get result from log

def gdb_reset():
	gdb_process.close()
	init_gdb()
	# Clear stack
