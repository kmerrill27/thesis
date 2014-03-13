from helper import *
from stackframe import *

class FrameWidget(QtGui.QFrame):

	def __init__(self):
		super(FrameWidget, self).__init__()
		self.initUI()

	def initUI(self):
		self.top_bar = FrameTopBar()
		self.window = FrameWindow()
		frameWrapVert(self, [self.top_bar, self.window])

	def clear(self):
		self.window.clear()

	def displayFrame(self, frame):
		self.window.displayFrame(frame)

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
		self.current_frame = None
		self.frame_display = None

	def initUI(self):
		self.frame = QtGui.QVBoxLayout()
		self.frame.addStretch()
		self.setLayout(self.frame)

	def displayFrame(self, frame):
		if frame != self.current_frame:
			if self.frame_display != None:
				self.frame_display.hide()
				self.frame.removeWidget(self.frame_display)
				self.frame_display.deleteLater()

			self.current_frame = frame
			self.frame_display = FrameDisplay(frame)
			self.frame.addWidget(self.frame_display)

	def clear(self):
		self.current_frame = None
		self.frame_display = None

		# First item is stretch - do not remove
		for i in range (1, self.frame.count()):
			self.frame.itemAt(i).widget().close()
			self.frame.takeAt(i)

