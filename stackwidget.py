from helper import *
from stackframe import *

class StackWidget(QtGui.QFrame):

	def __init__(self):
		super(StackWidget, self).__init__()
		self.stack = []
		self.initUI()

	def initUI(self):
		self.top_bar = StackTopBar()
		self.window = StackWindow()
		frameWrap(self, self.top_bar, self.window)

	def addFrame(self, frame):
		self.window.addFrame(frame.title)
		self.stack.append(frame)

	def removeFrame(self):
		frame = self.window.removeFrame()
		self.stack.pop()

class StackTopBar(QtGui.QWidget):

	def __init__(self):
		super(StackTopBar, self).__init__()
		self.initUI()

	def initUI(self):
		label = QtGui.QLabel()
		label.setText("Call Stack")

		box = QtGui.QHBoxLayout()
		box.addWidget(label)
		self.setLayout(box)

class StackWindow(QtGui.QWidget):

	def __init__(self, parent=None):
		super(StackWindow, self).__init__()
		self.initUI()

	def initUI(self):
		self.stack = QtGui.QVBoxLayout()
		self.stack.addStretch()
		self.stack.setSpacing(2)
		self.setLayout(self.stack)

		self.button_group = QtGui.QButtonGroup()

	def addFrame(self, label):
		frame = QtGui.QPushButton(label)
		frame.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		frame.setCheckable(True)
		frame.setChecked(True)

		self.button_group.addButton(frame)

		self.stack.insertWidget(0, frame, 2)

	def removeFrame(self):
		if (self.stack.count() > 0):
			frame = self.stack.itemAt(0).widget()
			frame.hide()
			self.stack.removeWidget(frame)
			self.button_group.removeButton(frame)

			if (self.stack.count() > 0 and self.button_group.checkedButton == 0):
				self.stack.itemAt(0).widget().setChecked(True)

