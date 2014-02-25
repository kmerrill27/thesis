import os
import platform
from widgets import *

class SourceCodeWidget(QtGui.QWidget):

	def __init__(self, source_code_window):
		super(SourceCodeWidget, self).__init__()
		self.main_window = source_code_window
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

		#os.system('gdb stackviz')
		#self.source_code_widget.highlightLine(0)

	def formatPath(self, filename):
		if (platform.system() == "Windows"):
			return filename.replace(" ", "%")
		else:
			# Unix
			return filename.replace(" ", "\ ").replace("'", "\'")

class SourceCodeWindow(QtGui.QListWidget):

	def __init__(self):
		super(SourceCodeWindow, self).__init__()

	def loadSource(self, filename):
		self.clear()

		if (self.isCSource(filename)):
			with open(filename) as f:
				source_lines = [line.rstrip('\n') for line in f]
			self.addItems(source_lines)
			return 1
		else:
			self.addItem("ERROR: not a C source file")
			self.highlightLine(0)
			return -1

	def highlightLine(self, line_num):
		self.setCurrentRow(line_num)

	def isCSource(self, filename):
		base_file = os.path.basename(filename)
		return base_file.endswith(".C") or base_file.endswith(".c")

	# Override to disallow user from selecting line
	def mousePressEvent(self, event):
		return

	# Override to disallow user from selecting line
	def mouseMoveEvent(self, event):
		return
