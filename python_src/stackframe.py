from PyQt4 import QtGui
from helper import *

class StackFrame:

	def __init__(self, title, frame_ptr, stack_ptr):
		self.title = title
		self.frame_ptr = frame_ptr
		self.stack_ptr = stack_ptr
		self.items = []

	def addItem(self, frame_item):
		self.items.insert(0, frame_item)

	def removeItem(self):
		self.items.pop()

class FrameItem:

	def __init__(self, title, addr, bytes, value):
		self.title = title
		self.addr = addr
		self.bytes = bytes
		self.value = value

class FrameDisplay(QtGui.QFrame):

	def __init__(self, frame):
		super(FrameDisplay, self).__init__()
		self.frame = frame
		self.initUI()

	def initUI(self):
		stack_ptr = QtGui.QLabel()
		stack_ptr.setText("Stack ptr: " + str(int(self.frame.stack_ptr, 16)))

		frame_ptr = QtGui.QLabel()
		frame_ptr.setText("Frame ptr: " + str(int(self.frame.frame_ptr, 16)))

		frame_disp = QtGui.QWidget()
		self.box = QtGui.QVBoxLayout()
		self.box.addStretch()
		self.updateDisplay()
		frame_disp.setLayout(self.box)

		frameWrapVert(self, [stack_ptr, frame_disp, frame_ptr])

	def updateDisplay(self):
		sorted_list = sorted(self.frame.items, key=lambda x: x.addr)
		for item in sorted_list:
			self.displayItem(item)

	def displayItem(self, frame_item):
		item_title = QtGui.QLabel()
		item_title.setText(frame_item.title + " (at " + str(int(frame_item.addr, 16)) + ") :")
		item_value = QtGui.QLabel()
		item_value.setText(str(frame_item.value))

		item_frame = QtGui.QFrame()
		frameWrapVert(item_frame, [item_title, item_value])

		self.box.addWidget(item_frame)
