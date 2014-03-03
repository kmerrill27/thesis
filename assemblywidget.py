from PyQt4 import QtGui
from helper import *

class AssemblyWidget(QtGui.QFrame):

	def __init__(self):
		super(AssemblyWidget, self).__init__()
		self.init_UI()

	def init_UI(self):
		self.top_bar = AssemblyTopBar()
		self.window = AssemblyWindow()
		frameWrapVert(self, [self.top_bar, self.window])

	def clear(self):
		self.window.clear()

	def displayLines(self, lines):
		self.window.displayLines(lines)

class AssemblyTopBar(QtGui.QWidget):

	def __init__(self):
		super(AssemblyTopBar, self).__init__()
		self.initUI()

	def initUI(self):
		label = QtGui.QLabel()
		label.setText("Assembly Code")

		box = QtGui.QHBoxLayout()
		box.addWidget(label)
		self.setLayout(box)

class AssemblyWindow(QtGui.QListWidget):

	def __init__(self):
		super(AssemblyWindow, self).__init__()

	def displayLines(self, lines):
		self.clear()
		lines = [line.rstrip('\n') for line in lines]
		self.addItems(lines)

	def highlightLine(self, line_num):
		self.setCurrentRow(line_num)

	# Override to disallow user from selecting line
	def mousePressEvent(self, event):
		return

	# Override to disallow user from selecting line
	def mouseMoveEvent(self, event):
		return
