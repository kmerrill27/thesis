from defs import *
from gdbprocess import *
from sourceandassemblywidget import *
from stackandframewidget import *

class StackVisualizer(QtGui.QWidget):
	""" Central StackExplorer widget for controlling all user interaction """

	def __init__(self):
		super(StackVisualizer, self).__init__()
		self.initUI()

	def initUI(self):
		grid = QtGui.QGridLayout(self)
		self.gdb_process = GDBProcess()

		# Initialize widget views
		self.source_and_assembly_widget = SourceAndAssemblyWidget()
		self.stack_and_frame_widget = StackAndFrameWidget(self.gdb_process, self.source_and_assembly_widget)
		self.source_and_assembly_widget.setStackAndFrameWidget(self.stack_and_frame_widget)

		self.toolbar = QtGui.QToolBar()
		self.setupToolbar()

		# Set up mode actions
		self.inspect_action = self.setupAction("Inspect", INSPECT_ICON, "Ctrl+Up", self.toggleInspect, True)
		self.inspect_cursor = self.getCursor(INSPECT_ICON)
		self.decimal_action = self.setupAction("Decimal", DECIMAL_ICON, "Ctrl+1", self.toggleDecimal, True)
		self.decimal_cursor = self.getCursor(DECIMAL_ICON)

		splitterWrapHoriz(grid, [self.stack_and_frame_widget, self.source_and_assembly_widget])
		grid.addWidget(self.toolbar)
		self.setLayout(grid)

	def setupToolbar(self):
		self.addSpacer()
		# On Mac OS X, Ctrl corresponds to Command key
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

		# Add action and label to toolbar
		self.toolbar.addAction(action)
		self.toolbar.addWidget(label)
		self.addSpacer()

		return action

	def addSpacer(self):
		# Add space block between toolbar elements
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
						frame = self.gdb_process.gdbUpdateTopFrame(self.stack_and_frame_widget.getTopFrame())
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

			# Restart program and add main frame
			self.reset()
			new_frame = self.gdb_process.startProcess()
			self.stack_and_frame_widget.addFrame(new_frame)

			# Run program until end and update display
			self.gdb_process.gdbRun()
			self.finish()

			QtGui.QApplication.restoreOverrideCursor()

	def reset(self):
		if self.source_and_assembly_widget.isSource():
			QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

			# Clear all widgets and reset gdb process
			self.stack_and_frame_widget.reset()
			self.source_and_assembly_widget.clear()

			QtGui.QApplication.restoreOverrideCursor()

	def toggleDecimal(self, checked):
		if not checked:
			# Deselect decimal
			QtGui.QApplication.restoreOverrideCursor()
			self.stack_and_frame_widget.toggleDecimal(False)
		else:
			if self.inspect_action.isChecked():
				# Deselect inspect - only one of decimal and inspect allowed at a time
				QtGui.QApplication.restoreOverrideCursor()
				self.inspect_action.setChecked(False)
				self.stack_and_frame_widget.toggleInspect(False)

			# Select decimal
			QtGui.QApplication.setOverrideCursor(self.decimal_cursor)
			self.stack_and_frame_widget.toggleDecimal(True)

	def toggleInspect(self, checked):
		if not checked:
			# Deselect inspect
			QtGui.QApplication.restoreOverrideCursor()
			self.stack_and_frame_widget.toggleInspect(False)
		else:
			if self.decimal_action.isChecked():
				# Deselect decimal - only one of inspect and decimal allowed at a time
				QtGui.QApplication.restoreOverrideCursor()
				self.decimal_action.setChecked(False)
				self.stack_and_frame_widget.toggleDecimal(False)

			# Select inspect
			QtGui.QApplication.setOverrideCursor(self.inspect_cursor)
			self.stack_and_frame_widget.toggleInspect(True)

	def getNextFrame(self):
		if self.gdb_process.process:
			# Program has already started
			[new_frame, retval] = self.gdb_process.gdbFunctionStep()
			if new_frame and not self.gdb_process.returningFromMain(new_frame):
				# "Run" previous frame on stack to function call
				self.gdb_process.gdbUpdatePreviousFrame(self.stack_and_frame_widget.getTopFrame())
		elif self.reset:
			# Start program
			return [self.gdb_process.gdbInit(), None]

		return [new_frame, retval]

	def finish(self):
			# Set display to last line of main
			frame = self.gdb_process.gdbUpdateTopFrame(self.stack_and_frame_widget.getTopFrame())
			self.source_and_assembly_widget.setLine(frame.line, frame.assembly)
			# Run program until end for exit status
			exit_status = self.gdb_process.gdbFinishUp()
			# Display exit status and set self.stack_and_frame_widget.finished to True
			self.stack_and_frame_widget.finish(exit_status, frame)

	def getCursor(self, icon):
		# Create custom cursor from image file
		img = QtGui.QImage(icon)
		pixmap = QtGui.QPixmap.fromImage(img)
		pixmap = pixmap.scaled(CURSOR_SIZE, CURSOR_SIZE, QtCore.Qt.KeepAspectRatio)
		return QtGui.QCursor(pixmap, -1, -1)
