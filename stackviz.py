from stackandframe import *
from sourcewidget import *

class StackVisualizer(QtGui.QWidget):

	def __init__(self):
		super(StackVisualizer, self).__init__()
		self.initUI()

	def initUI(self):
		grid = QtGui.QGridLayout(self)

		self.stack_and_frame_widget = StackAndFrameWidget()
		self.source_widget = SourceWidget()

		# Testing
		for i in range(0, 5):
			frame = StackFrame("Frame " + str(i))
			self.stack_and_frame_widget.addFrame(frame)
		self.stack_and_frame_widget.removeFrame()

		horiz_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
		horiz_splitter.addWidget(self.stack_and_frame_widget)
		horiz_splitter.addWidget(self.source_widget)

		grid.addWidget(horiz_splitter)
		self.setLayout(grid)

	def highlightSourceLine(self, line_num):
		self.source_window.highlightLine(line_num)
