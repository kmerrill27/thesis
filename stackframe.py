from PyQt4 import QtGui
from helper import *

class StackFrame:

	def __init__(self, title):
		self.title = title

class FrameDisplay(QtGui.QFrame):

	def __init__(self, frame):
		super(FrameDisplay, self).__init__()
		self.frame = frame
		self.initUI()

	def initUI(self):
		title = QtGui.QLabel()
		title.setText(self.frame.title)
		frame_disp = QtGui.QWidget()
		frameWrapVert(self, title, frame_disp)
