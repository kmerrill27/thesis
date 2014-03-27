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

		self.inspect_action = self.setupAction("Inspect", INSPECT_ICON, "Ctrl+Up", self.toggleInspect, True)
		self.inspect_cursor = self.getCursor(INSPECT_ICON)
		self.decimal_action = self.setupAction("Decimal", DECIMAL_ICON, "Ctrl+1", self.toggleDecimal, True)
		self.decimal_cursor = self.getCursor(DECIMAL_ICON)

		splitterWrapHoriz(grid, [self.stack_and_frame_widget, self.source_and_assembly_widget])
		grid.addWidget(self.toolbar)
		self.setLayout(grid)

	def setupToolbar(self):
		# On Mac OS X, Ctrl corresponds to Command key
		self.addSpacer()
		self.setupAction("Line step", LINE_ICON, "Right", self.lineStep, False)
		self.setupAction("Function step", FUNCTION_ICON, "Ctrl+Right", self.functionStep, False)
		self.setupAction("Run", RUN_ICON, "Space", self.run, False)
		self.setupAction("Reset", RESET_ICON, "Ctrl+Left", self.reset, False)

	def setupAction(self, name, icon, shortcut, handler, checkable):
		action = QtGui.QAction(QtGui.QIcon(icon), name, self)
		action.setShortcut(QtGui.QKeySequence(shortcut))
		action.setStatusTip(name)
		action.setCheckable(checkable)
		action.triggered.connect(handler)
		label = QtGui.QLabel()
		label.setText(name)
		self.toolbar.addAction(action)
		self.toolbar.addWidget(label)
		self.addSpacer()

		return action

	def addSpacer(self):
		spacer = QtGui.QWidget()
		spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		self.toolbar.addWidget(spacer)

	def lineStep(self):
		if not self.stack_and_frame_widget.finished and self.source_and_assembly_widget.isSource():

			QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

			if self.gdb_process.process:
				# Program has already started
				[returned, retval] = self.gdb_process.gdbLineStep()

				if returned:
					# Returned from function
					self.stack_and_frame_widget.returned(retval)
				else:
					if retval:
						if self.gdb_process.hitFinalBreakpoint(retval):
							# Hit final breakpoint in main
							self.finish()
						else:
							# Stepped into different function
							new_frame = self.gdb_process.functionSetup()
							self.stack_and_frame_widget.addFrame(new_frame)
					else:
						# Inside same function
						frame = self.gdb_process.gdbUpdateCurrentFrame(self.stack_and_frame_widget.getTopFrame())
						self.stack_and_frame_widget.updateFrame(frame)

			elif self.reset:
				# Start program
				new_frame = self.gdb_process.gdbInit()
				self.stack_and_frame_widget.addFrame(new_frame)

			QtGui.QApplication.restoreOverrideCursor()

	def functionStep(self):
		if not self.stack_and_frame_widget.finished and self.source_and_assembly_widget.isSource():

			QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

			[new_frame, retval] = self.getNextFrame()

			if self.gdb_process.returningFromMain(new_frame):
				# No more function calls - hit return breakpoint in main
				self.finish()
			elif new_frame:
				# Stepped into function
				self.stack_and_frame_widget.addFrame(new_frame)
			else:
				# Returned from function
				self.stack_and_frame_widget.returned(retval)

		QtGui.QApplication.restoreOverrideCursor()

	def run(self):
		if not self.stack_and_frame_widget.finished and self.source_and_assembly_widget.isSource():
			QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

			if self.gdb_process.process:
				self.stack_and_frame_widget.setToMainFrame()
			else:
				new_frame = self.gdb_process.startProcess()
				self.stack_and_frame_widget.addFrame(new_frame)

			self.gdb_process.gdbRun()
			self.finish()

			QtGui.QApplication.restoreOverrideCursor()

	def reset(self):
		if self.source_and_assembly_widget.isSource():
			QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

			self.stack_and_frame_widget.reset()
			self.source_and_assembly_widget.clear()

			QtGui.QApplication.restoreOverrideCursor()

	def toggleDecimal(self, checked):
		if not checked:
			QtGui.QApplication.restoreOverrideCursor()
			self.stack_and_frame_widget.toggleDecimal(False)
		else:
			if self.inspect_action.isChecked():
				QtGui.QApplication.restoreOverrideCursor()
				self.inspect_action.setChecked(False)
				self.stack_and_frame_widget.toggleInspect(False)

			QtGui.QApplication.setOverrideCursor(self.decimal_cursor)
			self.stack_and_frame_widget.toggleDecimal(True)

	def toggleInspect(self, checked):
		if not checked:
			QtGui.QApplication.restoreOverrideCursor()
			self.stack_and_frame_widget.toggleInspect(False)
		else:
			if self.decimal_action.isChecked():
				QtGui.QApplication.restoreOverrideCursor()
				self.decimal_action.setChecked(False)
				self.stack_and_frame_widget.toggleDecimal(False)

			QtGui.QApplication.setOverrideCursor(self.inspect_cursor)
			self.stack_and_frame_widget.toggleInspect(True)

	def getNextFrame(self):
		if self.gdb_process.process:
			# Program has already started
			[new_frame, retval] = self.gdb_process.gdbFunctionStep()
			if new_frame and not self.gdb_process.returningFromMain(new_frame):
				# "Run" previous frame on stack to function call
				self.gdb_process.gdbUpdateFrame(self.stack_and_frame_widget.getTopFrame())
		elif self.reset:
			# Start program
			return [self.gdb_process.gdbInit(), None]

		return [new_frame, retval]

	def finish(self):
			frame = self.gdb_process.gdbUpdateCurrentFrame(self.stack_and_frame_widget.getCurrentFrame())
			self.source_and_assembly_widget.setLine(frame.line, frame.assembly)
			exit_status = self.gdb_process.gdbFinishUp()
			self.stack_and_frame_widget.finish(exit_status, frame)

	def getCursor(self, icon):
		img = QtGui.QImage(icon)
		pixmap = QtGui.QPixmap.fromImage(img)
		pixmap = pixmap.scaled(32, 32, QtCore.Qt.KeepAspectRatio)
		return QtGui.QCursor(pixmap, -1, -1)
