import os
import platform

from stackandframewidget import *

class SourceWidget(QtGui.QFrame):
	""" Widget for displaying source code """

	def __init__(self, gdb_process, assembly_widget):
		super(SourceWidget, self).__init__()
		self.gdb_process = gdb_process
		self.assembly_widget = assembly_widget
		self.initUI()

	def initUI(self):
		self.window = SourceWindow()
		self.top_bar = SourceTopBar(self.gdb_process, self.assembly_widget, self.window)
		frameWrapVert(self, [self.top_bar, self.window])

	def setStackAndFrameWidget(self, stack_and_frame_widget):
		""" Stack and frame widget must be set before any function called """
		self.top_bar.setStackAndFrameWidget(stack_and_frame_widget)

	def highlightLine(self, line_num):
		self.window.highlightLine(int(line_num))

	def clear(self):
		self.window.unhighlightLines()

class SourceTopBar(QtGui.QWidget):
	""" Menu bar for source widget label and source file picker """

	def __init__(self, gdb_process, assembly_widget, source_window):
		super(SourceTopBar, self).__init__()
		self.gdb_process = gdb_process
		self.assembly_widget = assembly_widget
		self.source_window = source_window
		self.stack_and_frame_widget = None
		self.initUI()

	def initUI(self):
		label = QtGui.QLabel()
		label.setText(SOURCE_WIDGET_TITLE)

		self.current_file = QtGui.QLabel()
		self.current_file.setText(NO_SOURCE_FILE)

		file_button = QtGui.QPushButton(LOAD_SOURCE_MESSAGE)
		file_button.clicked.connect(self.fileButtonClicked)

		box = QtGui.QHBoxLayout()
		box.addWidget(label)
		box.addWidget(self.current_file)
		box.addWidget(file_button)
		self.setLayout(box)

	def setStackAndFrameWidget(self, stack_and_frame_widget):
		""" Stack and frame widget must be set before any functions called """
		self.stack_and_frame_widget = stack_and_frame_widget

	def fileButtonClicked(self):
		""" On file picker trigger, get user-selected source file """
		filename = QtGui.QFileDialog.getOpenFileName(self, SELECT_FILE_MESSAGE)
		if filename:
			# User selected a file
			self.current_file.setText(os.path.basename(str(filename)))
			err = self.source_window.loadSource(str(filename))
			self.assembly_widget.clear()
			self.stack_and_frame_widget.clear()
			self.gdb_process.gdbReset()

			if (err > 0):
				# User selected a valid C source file
				self.compileSource(str(filename))

	def compileSource(self, filename):
		""" Compile C source file """
		if (filename):
			command = C_COMPILE.format(self.formatPath(filename), C_OUT)
			os.system(command)

	def formatPath(self, filename):
		""" Format full pathname according to OS convention """
		if (platform.system() == WINDOWS):
			# Windows
			return filename.replace(" ", "%")
		else:
			# Unix
			return filename.replace(" ", "\ ").replace("'", "\'")

class SourceWindow(QtGui.QListWidget):
	""" Window for displaying source program """

	def __init__(self):
		super(SourceWindow, self).__init__()
		self.isSource = False

	def loadSource(self, filename):
		""" Load and display lines of source file """
		self.clear()

		if (self.isCSource(filename)):
			# Read in all lines from source file
			with open(filename) as f:
				source_lines = [line.rstrip('\n') for line in f]
			self.addItems(source_lines)
			self.unhighlightLines()
			self.isSource = True
			return 1
		else:
			# File not a C source file - display error message
			self.addItem(NOT_C_SOURCE)
			self.isSource = False
			return -1

	def highlightLine(self, line_num):
		""" Highlight specified line """
		self.setCurrentRow(line_num-1)
		self.scrollToItem(self.item(line_num-1))

	def unhighlightLines(self):
		""" Remove highlight from all lines """
		self.setCurrentRow(-1)
		self.scrollToItem(self.item(0))

	def isCSource(self, filename):
		""" Check if file is a C source file """
		base_file = os.path.basename(filename)
		return base_file.endswith(".C") or base_file.endswith(".c")

	def keyPressEvent(self, event):
		""" Override to disallow user from selecting line """
		return

	def mousePressEvent(self, event):
		""" Override to disallow user from selecting line """
		return

	def mouseMoveEvent(self, event):
		""" Override to disallow user from selecting line """
		return
