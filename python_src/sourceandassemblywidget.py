from assemblywidget import *
from sourcewidget import *

class SourceAndAssemblyWidget(QtGui.QFrame):

	def __init__(self):
		super(SourceAndAssemblyWidget, self).__init__()
		self.initUI()

	def initUI(self):
		self.assembly_widget = AssemblyWidget()
		self.source_widget = SourceWidget(self.assembly_widget)

		grid = QtGui.QGridLayout(self)
		splitterWrapVert(grid, [self.source_widget, self.assembly_widget])
		self.setLayout(grid)

	def setStackAndFrameWidget(self, stack_and_frame_widget):
		self.source_widget.setStackAndFrameWidget(stack_and_frame_widget)

	def setLine(self, line_num, assembly):
		self.source_widget.highlightLine(line_num)
		self.assembly_widget.displayLines(assembly)

	def clear(self):
		self.source_widget.clear()
		self.assembly_widget.clear()

	def isSource(self):
		return self.source_widget.window.isSource
