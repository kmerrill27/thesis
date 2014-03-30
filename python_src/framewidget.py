from stackframe import *

class FrameWidget(QtGui.QFrame):
	""" Widget for displaying selected stack frame """

	def __init__(self):
		super(FrameWidget, self).__init__()
		self.initUI()

	def initUI(self):
		self.retval_box = QtGui.QLineEdit()
		self.retval_box.setReadOnly(True)

		self.addr_box = QtGui.QLineEdit()
		self.addr_box.setReadOnly(True)

		self.window = FrameWindow(self.addr_box)

		self.top_bar = FrameTopBar(self.window)

		frameWrapVert(self, [self.top_bar, self.retval_box, self.addr_box, self.window])

	def flip(self, checked):
		self.window.flip(checked)

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

class FrameTopBar(QtGui.QWidget):
	""" Menu bar for frame widget label """

	def __init__(self, frame_window):
		super(FrameTopBar, self).__init__()
		self.frame_window = frame_window
		self.initUI()

	def initUI(self):
		self.button_group = QtGui.QButtonGroup()
		self.button_group.buttonClicked.connect(self.modeSwitched)

		label = QtGui.QLabel()
		label.setText(FRAME_WIDGET_TITLE)

		box = QtGui.QHBoxLayout()
		box.addWidget(label)
		box.addSpacing(10)
		box.setSpacing(5)

		# Buttons for controlling display mode for frame items
		self.addButton(HEX_ICON, HEX_MODE, box).setChecked(True)
		self.addButton(DECIMAL_ICON, DECIMAL_MODE, box)
		self.addButton(ZOOM_ICON, ZOOM_MODE, box)

		self.setLayout(box)

	def addButton(self, icon, mode, box):
		""" Set up mode buttons """
		button = QtGui.QPushButton()
		button.setCheckable(True)
		button.setIcon(QtGui.QIcon(icon))
		button.setToolTip(mode)
		button.setMaximumWidth(BUTTON_WIDTH)

		self.button_group.addButton(button)
		box.addWidget(button)

		return button

	def modeSwitched(self):
		""" Change mode between hexadecimal, decimal, and zoom value """
		self.frame_window.setMode(self.button_group.checkedButton().toolTip())

class FrameWindow(QtGui.QWidget):
	""" Window for displaying selected stack frame info """

	def __init__(self, addr_box):
		super(FrameWindow, self).__init__()
		self.initUI()
		self.addr_box = addr_box
		self.current_frame = None
		self.frame_display = None
		self.base_label = None
		self.mode = None
		self.reverse = False

	def initUI(self):
		self.frame = QtGui.QVBoxLayout()
		self.frame.addStretch()
		self.frame.setDirection(QtGui.QBoxLayout.TopToBottom)
		self.setLayout(self.frame)

	def flip(self, checked):
		""" Reverse stack to grow up or down """
		self.reverse = checked
		if self.reverse:
			self.frame.setDirection(QtGui.QBoxLayout.BottomToTop)
		else:
			self.frame.setDirection(QtGui.QBoxLayout.TopToBottom)
		
		if self.current_frame:
			reverse_row = self.frame_display.rowCount() - 1 - self.current_frame.selected_row 
			self.displayFrame(self.current_frame)
			self.frame_display.selectRow(reverse_row)

	def displayFrame(self, frame):
		""" Display frame items """
		if self.frame_display != None:
			# Clear current display
			self.clear()

		self.current_frame = frame
		self.frame_display = FrameDisplay(frame, self.addr_box, self.mode, self.reverse)
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

		self.current_frame = None
		self.frame_display = None
		self.base_label = None

	def removeItem(self, item):
		""" Remove frame item from display """
		if item:
			item.hide()
			self.frame.removeWidget(item)
			item.deleteLater()

	def setMode(self, mode):
		if self.frame_display:
			self.frame_display.setMode(mode)
		self.mode = mode
