from stackframe import *

class FrameWidget(QtGui.QFrame):
	""" Widget for displaying selected stack frame """

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

	def displayFrame(self, frame):
		""" Display stack frame in window """
		self.window.displayFrame(frame)

	def returned(self, retval):
		""" Display (possibly void) function return value """
		if retval:
			self.retval_box.setText(RETURNED_WITH.format(retval))
		else:
			self.retval_box.setText(RETURNED_VOID)

	def finish(self, exit_status, frame):
		""" Display program execution completed message """
		self.retval_box.setText(PROGRAM_FINISHED.format(exit_status))
		self.displayFrame(frame)

	def clear(self):
		""" Clear frame display and message boxes """
		self.clearBoxes()
		self.window.clear()

	def clearBoxes(self):
		""" Clear message boxes """
		self.retval_box.clear()
		self.addr_box.clear()

	def toggleDecimal(self, decimal_on):
		""" Toggle decimal mode, which displays address as hex or dec """
		self.window.toggleDecimal(decimal_on)

	def toggleInspect(self, inspectOn):
		""" Toggle inspect mode, which displays struct zoom values """
		self.window.toggleInspect(inspectOn)

class FrameTopBar(QtGui.QWidget):
	""" Menu bar for frame widget label """

	def __init__(self):
		super(FrameTopBar, self).__init__()
		self.initUI()

	def initUI(self):
		label = QtGui.QLabel()
		label.setText(FRAME_WIDGET_TITLE)

		box = QtGui.QHBoxLayout()
		box.addWidget(label)

		self.setLayout(box)

class FrameWindow(QtGui.QWidget):
	""" Window for displaying selected stack frame info """

	def __init__(self, addr_box):
		super(FrameWindow, self).__init__()
		self.initUI()
		self.addr_box = addr_box
		self.frame_display = None
		self.base_label = None
		self.inspect_on = False
		self.decimal_on = False

	def initUI(self):
		self.frame = QtGui.QVBoxLayout()
		self.frame.addStretch()
		self.setLayout(self.frame)

	def displayFrame(self, frame):
		""" Display frame items """
		if self.frame_display != None:
			# Clear current display
			self.clear()

		self.frame_display = FrameDisplay(frame, self.addr_box, self.inspect_on, self.decimal_on)
		self.frame.addWidget(self.frame_display, 1)

		if frame.bottom:
			# Not in main - main has not base address label
			self.base_label = QtGui.QLabel()
			self.base_label.setText(FRAME_BOTTOM + frame.bottom)
			self.frame.addWidget(self.base_label)

	def clear(self):
		""" Clear display """
		self.removeItem(self.frame_display)
		self.removeItem(self.base_label)
		self.addr_box.clear()

		self.frame_display = None
		self.base_label = None

	def removeItem(self, item):
		""" Remove frame item from display """
		if item:
			item.hide()
			self.frame.removeWidget(item)
			item.deleteLater()

	def toggleDecimal(self, decimal_on):
		""" Toggle decimal mode, which displays address as hex or dec """
		if self.frame_display:
			self.frame_display.toggleDecimal(decimal_on)
		self.decimal_on = decimal_on

	def toggleInspect(self, inspect_on):
		""" Toggle inspect mode, which displays struct zoom values """
		if self.frame_display:
			self.frame_display.toggleInspect(inspect_on)
		self.inspect_on = inspect_on
