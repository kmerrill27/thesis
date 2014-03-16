import os
from defs import *

def disas(src_line):
	with open(DISAS_IFILE, 'r') as f:
		script = f.read()

	# Insert output file name and line number into gdb script
	script = script.replace(ARG1, DISAS_OFILE)
	script = script.replace(ARG2, str(src_line))

	with open(SCRIPT_FILE, 'w') as f:
		f.write(script)

	# Run script against GDB to collect assembly code for line
	os.system(RUN_SCRIPT.format(SCRIPT_FILE, C_OUT))
