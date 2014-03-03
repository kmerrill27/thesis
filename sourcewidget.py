import os
import subprocess
import platform
from stackandframewidget import *
from helper import *

class SourceWidget(QtGui.QFrame):

	def __init__(self, stack_and_frame_widget, assembly_widget):
		super(SourceWidget, self).__init__()
		self.stack_and_frame_widget = stack_and_frame_widget
		self.assembly_widget = assembly_widget
		self.initUI()

	def initUI(self):
		self.window = SourceWindow(self.stack_and_frame_widget, self.assembly_widget)
		self.top_bar = SourceTopBar(self.window)
		frameWrapVert(self, [self.top_bar, self.window])

class SourceTopBar(QtGui.QWidget):

	def __init__(self, source_window):
		super(SourceTopBar, self).__init__()
		self.main_window = source_window
		self.initUI()

	def initUI(self):
		label = QtGui.QLabel()
		label.setText("Source Code")

		self.current_file = QtGui.QLabel()
		self.current_file.setText("No source file")

		file_button = QtGui.QPushButton("Load source")
		file_button.clicked.connect(self.fileButtonClicked)

		box = QtGui.QHBoxLayout()
		box.addWidget(label)
		box.addWidget(self.current_file)
		box.addWidget(file_button)
		self.setLayout(box)

	def fileButtonClicked(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, "Select a C program")
		if filename:
			self.current_file.setText(os.path.basename(str(filename)))
			err = self.main_window.loadSource(str(filename))

			if (err > 0):
				self.prepareVis(str(filename))

	def prepareVis(self, filename):
		os.system("gcc -g " + self.formatPath(filename) + " -o stackviz")

		#os.system("gdb -q -x test.py")
		#self.source_code_widget.highlightLine(0)

	def formatPath(self, filename):
		if (platform.system() == "Windows"):
			return filename.replace(" ", "%")
		else:
			# Unix
			return filename.replace(" ", "\ ").replace("'", "\'")

class SourceWindow(QtGui.QListWidget):

	def __init__(self, stack_and_frame_widget, assembly_widget):
		super(SourceWindow, self).__init__()
		self.stack_and_frame_widget = stack_and_frame_widget
		self.assembly_widget = assembly_widget

	def loadSource(self, filename):
		self.clear()
		self.stack_and_frame_widget.clear()
		self.assembly_widget.clear()

		if (self.isCSource(filename)):
			with open(filename) as f:
				source_lines = [line.rstrip('\n') for line in f]
			self.addItems(source_lines)
			return 1
		else:
			self.addItem("ERROR: not a C source file")
			return -1

	def highlightLine(self, line_num):
		self.setCurrentRow(line_num)
		# TODO: load assembly lines
		lines = ["0x0000000100000e88 <+152>:	mov    -0x20(%rbp),%eax",
   				 "0x0000000100000e8b <+155>:	add    $0x1,%eax",
   				 "0x0000000100000e8e <+158>:	mov    -0x8(%rbp),%rcx",
   				 "0x0000000100000e92 <+162>:	mov    -0x10(%rbp),%edx",
   	  			 "0x0000000100000e95 <+165>:	mov    -0x14(%rbp),%esi",
   				 "0x0000000100000e98 <+168>:	mov    %rcx,%rdi",
   				 "0x0000000100000e9b <+171>:	mov    %esi,-0x28(%rbp)",
   				 "0x0000000100000e9e <+174>:	mov    %eax,%esi",
   				 "0x0000000100000ea0 <+176>:	mov    -0x28(%rbp),%ecx",
   				 "0x0000000100000ea3 <+179>:	callq  0x100000df0 <bin_search>",
   			     "0x0000000100000ea8 <+184>:	mov    %eax,%ecx",
   				 "0x0000000100000eaa <+186>:	mov    %ecx,-0x1c(%rbp)"]
		self.assembly_widget.displayLines(lines)

	def isCSource(self, filename):
		base_file = os.path.basename(filename)
		return base_file.endswith(".C") or base_file.endswith(".c")

	# Override to disallow user from selecting line
	def mousePressEvent(self, event):
		return

	# Override to disallow user from selecting line
	def mouseMoveEvent(self, event):
		return
