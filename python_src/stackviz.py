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
		self.source_and_assembly_widget = SourceAndAssemblyWidget()
		self.stack_and_frame_widget = StackAndFrameWidget(self.gdb_process, self.source_and_assembly_widget)
		self.source_and_assembly_widget.setStackAndFrameWidget(self.stack_and_frame_widget)
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

		[new_frame, retval] = self.getNextFrame()

		if new_frame and new_frame != self.gdb_process.empty_frame:
			# Stepped into function
			self.source_and_assembly_widget.setLine(new_frame.line, new_frame.assembly)
			self.stack_and_frame_widget.addFrame(new_frame)
		elif not self.stack_and_frame_widget.finished and new_frame == self.gdb_process.empty_frame:
			# No more function calls - hit return breakpoint in main
			self.finish()
		elif not self.stack_and_frame_widget.finished:
			# Returned from function
			self.stack_and_frame_widget.returned(retval)
			self.stack_and_frame_widget.removeFrame()

	def run(self):
		if not self.stack_and_frame_widget.finished:
			if self.gdb_process.process:
				self.stack_and_frame_widget.setToMainFrame()
			else:
				new_frame = self.gdb_process.startProcess()
				self.stack_and_frame_widget.addFrame(new_frame)

			self.gdb_process.gdbRun()
			self.finish()

	def reset(self):
		self.stack_and_frame_widget.reset()
		self.source_and_assembly_widget.clear()

	def getNextFrame(self):
		if self.gdb_process.process:
			# Program has already started
			[new_frame, retval] = self.gdb_process.gdbFunctionStep()
			if new_frame and new_frame != self.gdb_process.empty_frame:
				# "Run" previous frame on stack to function call
				self.gdb_process.gdbUpdateFrame(self.stack_and_frame_widget.getTopFrame())
		elif self.source_and_assembly_widget.isSource() and self.reset:
			# Start program
			return [self.gdb_process.gdbInit(), None]

		return [new_frame, retval]

	def finish(self):
			frame = self.gdb_process.gdbUpdateCurrentFrame(self.stack_and_frame_widget.getCurrentFrame())
			self.source_and_assembly_widget.setLine(frame.line, frame.assembly)
			exit_status = self.gdb_process.gdbFinishUp()
			self.stack_and_frame_widget.finish(exit_status, frame)
