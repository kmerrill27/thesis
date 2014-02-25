from stackwidget import *
from framewidget import *
from sourcewidget import *

class StackVisualizer(QtGui.QWidget):

	def __init__(self):
		super(StackVisualizer, self).__init__()
		self.initUI()

	def initUI(self):
		grid = QtGui.QGridLayout(self)

		self.stack_bar = StackGraphicsTopBar()
		self.stack_window = StackGraphicsWindow()
		self.stack_frame = FrameWrappedWidget(self.stack_bar, self.stack_window)

		self.frame_bar = FrameTopBar()
		self.frame_widget = FrameWidget()
		self.frame_frame = FrameWrappedWidget(self.frame_bar, self.frame_widget)

		self.source_frame = FrameWidget()

		horiz_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
		horiz_splitter.addWidget(self.stack_frame)
		horiz_splitter.addWidget(self.frame_frame)
		horiz_splitter.addWidget(self.source_frame)

		grid.addWidget(horiz_splitter)
		self.setLayout(grid)

	def highlightSourceLine(self, line_num):
		self.source_window.highlightLine(line_num)
