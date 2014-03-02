from stackframe import *
from stackwidget import *
from framewidget import *

class StackAndFrameWidget(QtGui.QFrame):

	def __init__(self):
		super(StackAndFrameWidget, self).__init__()
		self.initUI()

	def initUI(self):
		self.frame_widget = FrameWidget()

		self.top_bar = StackTopBar()
		self.stack_widget = StackWindow(self.frame_widget)
		self.stack_widget_frame = QtGui.QFrame()

		frameWrapVert(self.stack_widget_frame, self.top_bar, self.stack_widget)
		frameWrapHoriz(self, self.stack_widget_frame, self.frame_widget)

	def addFrame(self, frame):
		self.stack_widget.addFrame(frame)

	def removeFrame(self):
		frame = self.stack_widget.removeFrame()

	def clear(self):
		self.stack_widget.clear()
