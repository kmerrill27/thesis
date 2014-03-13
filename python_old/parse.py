from defs import *
from PyQt4 import QtCore

def parse_disas():
	lines = []
	remaining_lines = []
	with open(DISAS_OFILE) as f:
		line = f.readline()
		while line:
			# Look for =>, indicating start of assembly code
			# Assembly code should be the last thing in the file
			if line.startswith(ASSEMBLY_START):
				lines.append(line.replace(ASSEMBLY_START, "").strip())
				remaining_lines = [ln.lstrip().rstrip('\n') for ln in f.readlines()]
				break
			line = f.readline()
	
	# Must be a QStringList to add to widget - does not support batch append		
	for line in remaining_lines:
		lines.append(line)

	return lines
