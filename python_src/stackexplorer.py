from gdbprocess import *
from sourceandassemblywidget import *

class StackExplorerWidget(QtGui.QWidget):
	""" Central StackExplorer widget for controlling all user interaction """

	def __init__(self):
		super(StackExplorerWidget, self).__init__()
		self.initUI()

	def initUI(self):
		grid = QtGui.QGridLayout(self)
		self.gdb_process = GDBProcess()

		# Initialize widget views
		self.source_and_assembly_widget = SourceAndAssemblyWidget(self.gdb_process)
		self.stack_and_frame_widget = StackAndFrameWidget(self.source_and_assembly_widget)
		self.source_and_assembly_widget.setStackAndFrameWidget(self.stack_and_frame_widget)

		self.toolbar = QtGui.QToolBar()
		self.setupToolbar()

		splitterWrapHoriz(grid, [self.stack_and_frame_widget, self.source_and_assembly_widget])
		grid.addWidget(self.toolbar)
		self.setLayout(grid)

	def setupToolbar(self):
		""" Add user execution control actions to main app toolbar """
		self.addSpacer()
		self.setupAction(LINE_STEP_LABEL, LINE_ICON, LINE_STEP_SHORTCUT, self.lineStep)
		self.setupAction(FUNCTION_STEP_LABEL, FUNCTION_ICON, FUNCTION_STEP_SHORTCUT, self.functionStep)
		self.setupAction(RUN_LABEL, RUN_ICON, RUN_SHORTCUT, self.run)
		self.setupAction(RESET_LABEL, RESET_ICON, RESET_SHORTCUT, self.reset)

	def setupAction(self, name, icon, shortcut, handler):
		""" Add user action to main app toolbar """
		action = QtGui.QAction(QtGui.QIcon(icon), name, self)
		action.setShortcut(QtGui.QKeySequence(shortcut))
		action.setStatusTip(name)
		action.triggered.connect(handler)

		label = QtGui.QLabel()
		label.setText(name)

		# Add action and label to toolbar
		self.toolbar.addAction(action)
		self.toolbar.addWidget(label)
		self.addSpacer()

		return action

	def addSpacer(self):
		""" Add space block between toolbar elements """
		spacer = QtGui.QWidget()
		spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		self.toolbar.addWidget(spacer)

	def lineStep(self):
		""" Step into current program's next source line """
		if not self.gdb_process.finished and self.source_and_assembly_widget.isSource():

			QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

			if self.gdb_process.process:
				# Program has already started
				[new_frame, retval, exiting_main] = self.gdb_process.gdbLineStep(self.stack_and_frame_widget.peekFrame())

				if new_frame:
					if retval:
						# Stepped into function
						self.stack_and_frame_widget.pushFrame(new_frame)
					else:
						# Inside same function
						self.stack_and_frame_widget.updateTopFrame(new_frame)
				else:
					# Returned from function
					if exiting_main:
						# No more function calls - hit return breakpoint in main
						self.finish()
					else:
						# Returned from non-main function
						self.stack_and_frame_widget.returned(retval)

			elif self.reset:
				# Start program
				new_frame = self.gdb_process.gdbInit()
				self.stack_and_frame_widget.pushFrame(new_frame)

			QtGui.QApplication.restoreOverrideCursor()

	def functionStep(self):
		""" Step into current program's next function call """
		if not self.gdb_process.finished and self.source_and_assembly_widget.isSource():

			QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

			[new_frame, retval, exiting_main] = self.setUpNextFrame()

			if exiting_main:
				# No more function calls - hit return breakpoint in main
				self.finish()
			elif new_frame:
				# Stepped into function
				self.stack_and_frame_widget.pushFrame(new_frame)
			else:
				# Returned from function
				self.stack_and_frame_widget.returned(retval)

		QtGui.QApplication.restoreOverrideCursor()

	def run(self):
		""" Run current program to exit """
		if not self.gdb_process.finished and self.source_and_assembly_widget.isSource():
			QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

			# Restart program and add main frame
			self.reset()
			new_frame = self.gdb_process.startProcess()
			self.stack_and_frame_widget.pushFrame(new_frame)

			# Run program until end and update display
			self.gdb_process.gdbRun()
			self.finish()

			QtGui.QApplication.restoreOverrideCursor()

	def reset(self):
		""" Reset current program execution to start """
		if self.source_and_assembly_widget.isSource():
			QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

			# Clear all widgets and reset gdb process
			self.gdb_process.gdbReset()
			self.stack_and_frame_widget.clear()
			self.source_and_assembly_widget.clear()

			QtGui.QApplication.restoreOverrideCursor()

	def setUpNextFrame(self):
		""" Make next function call and populate new stack frame """
		if self.gdb_process.process:
			# Program has already started
			[new_frame, retval, exiting_main] = self.gdb_process.gdbFunctionStep()
			if new_frame:
				# "Run" previous frame on stack to function call
				self.gdb_process.gdbUpdatePreviousFrame(self.stack_and_frame_widget.peekFrame())
		elif self.reset:
			# Start program
			return [self.gdb_process.gdbInit(), None, False]

		return [new_frame, retval, exiting_main]

	def finish(self):
		""" Finish current program execution and exit """
		# Set display to last line of main
		frame = self.gdb_process.gdbUpdateTopFrame(self.stack_and_frame_widget.peekFrame())
		self.source_and_assembly_widget.setLine(frame.line, frame.assembly)
		# Run program until end for exit status
		exit_status = self.gdb_process.gdbFinishUp()
		# Display exit status
		self.stack_and_frame_widget.finish(exit_status, frame)
