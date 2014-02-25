from stackwidget import *
from framewidget import *
from sourcewidget import *

class StackVisualizer(QtGui.QWidget):

	def __init__(self):
		super(StackVisualizer, self).__init__()
		self.initUI()

	def initUI(self):
		grid = QtGui.QGridLayout(self)

		self.stack_widget = StackWidget()
		self.frame_widget = FrameWidget()
		self.source_widget = SourceCodeWidget()

		horiz_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
		horiz_splitter.addWidget(self.stack_widget)
		horiz_splitter.addWidget(self.frame_widget)
		horiz_splitter.addWidget(self.source_widget)

		grid.addWidget(horiz_splitter)
		self.setLayout(grid)

	def highlightSourceLine(self, line_num):
		self.source_window.highlightLine(line_num)
