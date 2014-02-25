from widgets import *

class StackWidget(QtGui.QFrame):

	def __init__(self):
		super(StackWidget, self).__init__()
		self.initUI()

	def initUI(self):
		self.top_bar = StackTopBar()
		self.window = StackWindow()
		frameWrap(self.top_bar, self.window)

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

		for i in range(0, 5):
			self.addFrame("Frame " + str(i))

	def addFrame(self, label):
		frame = QtGui.QPushButton(label)
		frame.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		frame.setCheckable(True)
		frame.setChecked(True)

		self.button_group.addButton(frame)

		self.stack.insertWidget(0, frame, 2)
