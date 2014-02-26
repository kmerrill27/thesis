from stackwidget import *
from framewidget import *

class StackAndFrameWidget(QtGui.QFrame):

	def __init__(self):
		super(StackAndFrameWidget, self).__init__()
		self.initUI()

	def initUI(self):
		self.stack_widget = StackWidget()
		self.frame_widget = FrameWidget()

		box = QtGui.QHBoxLayout()
		box.addWidget(self.stack_widget)
		box.addWidget(self.frame_widget)

		self.setFrameShape(QtGui.QFrame.StyledPanel)
		self.setLayout(box)

	def addFrame(self, frame):
		self.stack_widget.addFrame(frame)

	def removeFrame(self):
		self.stack_widget.removeFrame()