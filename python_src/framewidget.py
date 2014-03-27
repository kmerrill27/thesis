from helper import *
from stackframe import *

class FrameWidget(QtGui.QFrame):

	def __init__(self):
		super(FrameWidget, self).__init__()
		self.initUI()

	def initUI(self):
		self.top_bar = FrameTopBar()
		self.retval_box = QtGui.QLineEdit()
		self.retval_box.setReadOnly(True)
		self.addr_box = QtGui.QLineEdit()
		self.addr_box.setReadOnly(True)
		self.window = FrameWindow(self.addr_box)
		frameWrapVert(self, [self.top_bar, self.retval_box, self.addr_box, self.window])

	def returned(self, retval):
		if retval:
			self.retval_box.setText(RETURNED_WITH.format(retval))
		else:
			self.retval_box.setText(RETURNED_VOID)

	def finish(self, exit_status, frame):
		self.retval_box.setText(PROGRAM_FINISHED.format(exit_status))
		self.window.updateFrameDisplay(frame)

	def toggleDecimal(self, decimal_on):
		self.window.toggleDecimal(decimal_on)

	def toggleInspect(self, inspectOn):
		self.window.toggleInspect(inspectOn)

	def clearBoxes(self):
		self.retval_box.clear()
		self.addr_box.clear()

	def clear(self):
		self.clearBoxes()
		self.window.clear()

	def updateFrame(self, frame):
		self.window.updateFrameDisplay(frame)

	def displayFrame(self, frame):
		self.window.displayFrame(frame)

	def getCurrentFrame(self):
		return self.window.current_frame

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

	def __init__(self, addr_box):
		super(FrameWindow, self).__init__()
		self.initUI()
		self.addr_box = addr_box
		self.current_frame = None
		self.frame_display = None
		self.base_label = None
		self.inspect_on = False
		self.decimal_on = False

	def initUI(self):
		self.frame = QtGui.QVBoxLayout()
		self.frame.addStretch()
		self.setLayout(self.frame)

	def toggleDecimal(self, decimal_on):
		if self.frame_display:
			self.frame_display.toggleDecimal(decimal_on)
		self.decimal_on = decimal_on

	def toggleInspect(self, inspect_on):
		if self.frame_display:
			self.frame_display.toggleInspect(inspect_on)
		self.inspect_on = inspect_on

	def updateFrameDisplay(self, frame):
		self.current_frame = None
		self.displayFrame(frame)

	def displayFrame(self, frame):
		if frame != self.current_frame:
			if self.frame_display != None:
				self.clear()

			self.current_frame = frame
			self.frame_display = FrameDisplay(frame, self.addr_box, self.inspect_on, self.decimal_on)
			self.frame.addWidget(self.frame_display, 1)

			# Check if in main (will be None)
			if frame.bottom:
				self.base_label = QtGui.QLabel()
				self.base_label.setText("Frame bottom: " + frame.bottom)
				self.frame.addWidget(self.base_label)

	def clear(self):
		self.removeItem(self.frame_display)
		self.removeItem(self.base_label)
		self.addr_box.clear()

		self.frame_display = None
		self.base_label = None
		self.current_frame = None

	def removeItem(self, item):
		if item:
			item.hide()
			self.frame.removeWidget(item)
			item.deleteLater()
