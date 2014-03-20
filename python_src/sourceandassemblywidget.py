from sourcewidget import *
from assemblywidget import *

class SourceAndAssemblyWidget(QtGui.QFrame):

	def __init__(self, gdb_process, stack_and_frame_widget):
		super(SourceAndAssemblyWidget, self).__init__()
		self.gdb_process = gdb_process
		self.stack_and_frame_widget = stack_and_frame_widget
		self.initUI()

	def initUI(self):
		self.assembly_widget = AssemblyWidget()
		self.source_widget = SourceWidget(self.gdb_process, self.stack_and_frame_widget, self.assembly_widget)

		grid = QtGui.QGridLayout(self)
		splitterWrapVert(grid, [self.source_widget, self.assembly_widget])
		self.setLayout(grid)

	def highlightLine(self, line_num):
		self.source_widget.highlightLine(line_num)

	def reset(self):
		self.source_widget.reset()
