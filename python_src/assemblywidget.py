from defs import *
from PyQt4 import QtCore
from PyQt4 import QtGui
from widgetwrapper import *

class AssemblyWidget(QtGui.QFrame):
	""" Widget for assembly instructions """

	def __init__(self):
		super(AssemblyWidget, self).__init__()
		self.init_UI()

	def init_UI(self):
		self.top_bar = AssemblyTopBar()
		self.window = AssemblyWindow()
		frameWrapVert(self, [self.top_bar, self.window])

	def displayLines(self, lines):
		self.window.displayLines(lines)

	def clear(self):
		self.window.clear()

class AssemblyTopBar(QtGui.QWidget):
	""" Menu bar for assembly widget label """

	def __init__(self):
		super(AssemblyTopBar, self).__init__()
		self.initUI()

	def initUI(self):
		label = QtGui.QLabel()
		label.setText(ASSEMBLY_WIDGET_TITLE)

		box = QtGui.QHBoxLayout()
		box.addWidget(label)
		self.setLayout(box)

class AssemblyWindow(QtGui.QListWidget):
	""" Window for displaying assembly instructions """

	def __init__(self):
		super(AssemblyWindow, self).__init__()

	def displayLines(self, lines):
		self.clear()
		self.addItems(lines)

	def highlightLine(self, line_num):
		self.setCurrentRow(line_num)

	def keyPressEvent(self, event):
		""" Override to disallow user from selecting line """
		return

	def mousePressEvent(self, event):
		""" Override to disallow user from selecting line """
		return

	def mouseMoveEvent(self, event):
		""" Override to disallow user from selecting line """
		return
