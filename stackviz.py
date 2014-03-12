from sourceandassemblywidget import *
from stackandframewidget import *
from defs import *

class StackVisualizer(QtGui.QWidget):

	def __init__(self):
		super(StackVisualizer, self).__init__()
		self.initUI()

	def initUI(self):
		grid = QtGui.QGridLayout(self)

		self.stack_and_frame_widget = StackAndFrameWidget()
		self.source_and_assembly_widget = SourceAndAssemblyWidget(self.stack_and_frame_widget)
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

		splitterWrapHoriz(grid, [self.stack_and_frame_widget, self.source_and_assembly_widget])
		grid.addWidget(self.toolbar)
		self.setLayout(grid)

	def setupToolbar(self):
		# On Mac OS X, Ctrl corresponds to Command key
		self.addSpacer()
		self.setupAction("Line step", ARROW_ICON, "Right", self.lineStep)
		self.setupAction("Function step", ARROW_ICON, "Ctrl+Right", self.functionStep)
		self.setupAction("Run", ARROW_ICON, "Space", self.run)
		self.setupAction("Reset", ARROW_ICON, "Ctrl+Left", self.reset)

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
