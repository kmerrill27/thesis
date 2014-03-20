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
		self.base_label = None

	def initUI(self):
		self.frame = QtGui.QVBoxLayout()
		self.frame.addStretch()
		self.setLayout(self.frame)

	def displayFrame(self, frame):
		self.frame.removeWidget
		if frame != self.current_frame:
			if self.frame_display != None:
				self.clear()

			self.current_frame = frame
			self.frame_display = FrameDisplay(frame)
			self.base_label = QtGui.QLabel()
			self.base_label.setText("Frame bottom: " + frame.bottom)
			self.frame.addWidget(self.frame_display, 1)
			self.frame.addWidget(self.base_label)

	def clear(self):
		self.removeItem(self.frame_display)
		self.removeItem(self.base_label)

		self.frame_display = None
		self.base_label = None

	def removeItem(self, item):
		if item:
			item.hide()
			self.frame.removeWidget(item)
			item.deleteLater()
