from widgets import *

class FrameWidget(QtGui.QFrame):

	def __init__(self):
		super(FrameWidget, self).__init__()
		self.initUI()

	def initUI(self):
		self.source_window = SourceCodeWindow()
		self.source_top_bar = SourceCodeWidget(self.source_window)
		frameWrap(source_widget, source_window)

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