from sourceandassemblywidget import *
from stackandframewidget import *
from runstate import *
from defs import *

class StackVisualizer(QtGui.QWidget):

	def __init__(self):
		super(StackVisualizer, self).__init__()
		self.initUI()

	def initUI(self):
		grid = QtGui.QGridLayout(self)

		self.gdb_process = GDBProcess()
		self.stack_and_frame_widget = StackAndFrameWidget(self.gdb_process)
		self.source_and_assembly_widget = SourceAndAssemblyWidget(self.stack_and_frame_widget)
		self.toolbar = QtGui.QToolBar()
		self.setupToolbar()

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
		if self.gdb_process.process:
			print "line"

	def functionStep(self):
		print "function"
		# TODO: Check if source loaded?
		if self.gdb_process.process:
			[new_frame, src_line, assembly] = self.gdb_process.gdbFunctionStep()
		else:
			[new_frame, src_line, assembly] = self.gdb_process.gdbInit()

		self.stack_and_frame_widget.addFrame(new_frame)
		self.source_and_assembly_widget.setLine(src_line, assembly)

	def run(self):
		if self.gdb_process.process:
			self.gdb_process.gdbRun()
			print "run"

	def reset(self):
		# Check if source loaded
		if self.gdb_process.process:
			self.stack_and_frame_widget.clear()
			self.source_and_assembly_widget.reset()
			self.gdb_process.gdbReset()

	def highlightSourceLine(self, line_num):
		if self.gdb_process.process:
			self.source_window.highlightLine(line_num)
