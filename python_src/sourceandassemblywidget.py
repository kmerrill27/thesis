from assemblywidget import *
from sourcewidget import *

class SourceAndAssemblyWidget(QtGui.QFrame):
	""" Widget for displaying source code and assembly instructions """

	def __init__(self, gdb_process):
		super(SourceAndAssemblyWidget, self).__init__()
		self.gdb_process = gdb_process
		self.initUI()

	def initUI(self):
		self.assembly_widget = AssemblyWidget()
		self.source_widget = SourceWidget(self.gdb_process, self.assembly_widget)

		grid = QtGui.QGridLayout(self)
		splitterWrapVert(grid, [self.source_widget, self.assembly_widget])
		self.setLayout(grid)

	def setStackAndFrameWidget(self, stack_and_frame_widget):
		""" Stack and frame widget must be set before any functions called """
		self.source_widget.setStackAndFrameWidget(stack_and_frame_widget)

	def setLine(self, line_num, assembly):
		""" Highlight source line and display corresponding assembly instructions """
		self.source_widget.highlightLine(line_num)
		self.assembly_widget.displayLines(assembly)

	def clear(self):
		""" Clear source and assembly display """
		self.source_widget.clear()
		self.assembly_widget.clear()

	def isSource(self):
		""" Return true if valid source file is loaded """
		return self.source_widget.window.is_source
