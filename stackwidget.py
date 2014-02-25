from widgets import *

class StackGraphicsTopBar(QtGui.QWidget):

	def __init__(self):
		super(StackGraphicsTopBar, self).__init__()
		self.initUI()

	def initUI(self):
		label = QtGui.QLabel()
		label.setText("Call Stack")

		box = QtGui.QHBoxLayout()
		box.addWidget(label)
		self.setLayout(box)

class StackGraphicsWindow(QtGui.QWidget):

	def __init__(self, parent=None):
		super(StackGraphicsWindow, self).__init__()
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
