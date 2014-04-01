from defs import *
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
		""" Display assembly instructions in window """
		self.window.displayLines(lines)

	def clear(self):
		""" Clear display """
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
		""" Display assembly instructions """
		self.clear()
		self.addItems(lines)
		# Highlight top row, which is current instruction
		self.setCurrentRow(0)

	def keyPressEvent(self, event):
		""" Override to disallow user from selecting line """
		return

	def mousePressEvent(self, event):
		""" Override to disallow user from selecting line """
		return

	def mouseMoveEvent(self, event):
		""" Override to disallow user from selecting line """
		return
