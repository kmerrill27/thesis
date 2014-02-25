from widgets import *

class FrameWidget(QtGui.QFrame):

	def __init__(self):
		super(FrameWidget, self).__init__()
		self.initUI()

	def initUI(self):
		self.top_bar = FrameTopBar()
		self.window = FrameWindow()
		frameWrap(self, self.top_bar, self.window)

class FrameTopBar(QtGui.QWidget):

	def __init__(self):
		super(FrameTopBar, self).__init__()
		self.initUI()

	def initUI(self):
		label = QtGui.QLabel()
		label.setText("Stack Frame")

		box = QtGui.QHBoxLayout()
		box.addWidget(label)
		self.setLayout(box)

class FrameWindow(QtGui.QWidget):

	def __init__(self):
		super(FrameWindow, self).__init__()
		self.initUI()

	def initUI(self):
		return