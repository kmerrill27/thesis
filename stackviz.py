from sourcewidget import *
from stackandframewidget import *

class StackVisualizer(QtGui.QWidget):

	def __init__(self):
		super(StackVisualizer, self).__init__()
		self.initUI()

	def initUI(self):
		grid = QtGui.QGridLayout(self)

		self.stack_and_frame_widget = StackAndFrameWidget()
		self.source_widget = SourceWidget(self.stack_and_frame_widget)
		self.toolbar = QtGui.QToolBar()
		self.setupToolbar()

		# Testing
		for i in range(0, 10):
			frame = StackFrame("Frame " + str(i), "0x0214321432", "0x243214123")
			frame.addItem(FrameItem("Callee Registers", "0x034039283", 4))
			frame.addItem(FrameItem("Return value", "0x034039283", 4))
			frame.addItem(FrameItem("Local vars", "0x034039283", 4))
			self.stack_and_frame_widget.addFrame(frame)
		self.stack_and_frame_widget.removeFrame()

		horiz_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
		horiz_splitter.addWidget(self.stack_and_frame_widget)
		horiz_splitter.addWidget(self.source_widget)

		grid.addWidget(horiz_splitter)
		grid.addWidget(self.toolbar)
		self.setLayout(grid)

	def setupToolbar(self):
		# On Mac OS X, Ctrl corresponds to Command key
		self.addSpacer()
		self.setupAction("Line step", "arrow.png", "Right", self.lineStep)
		self.setupAction("Function step", "arrow.png", "Ctrl+Right", self.functionStep)
		self.setupAction("Run", "arrow.png", "Space", self.run)
		self.setupAction("Reset", "arrow.png", "Ctrl+Left", self.reset)

	def setupAction(self, name, icon, shortcut, handler):
		action = QtGui.QAction(QtGui.QIcon(icon), name, self)
		action.setShortcut(QtGui.QKeySequence(shortcut))
		action.setStatusTip(name)
		action.triggered.connect(handler)
		label = QtGui.QLabel()
		label.setText(name)
		self.toolbar.addAction(action)
		self.toolbar.addWidget(label)
		self.addSpacer()

	def addSpacer(self):
		spacer = QtGui.QWidget()
		spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		self.toolbar.addWidget(spacer)

	def lineStep(self):
		print "line"

	def functionStep(self):
		print "function"

	def run(self):
		print "run"

	def reset(self):
		print "reset"
		self.stack_and_frame_widget.clear()

	def highlightSourceLine(self, line_num):
		self.source_window.highlightLine(line_num)
