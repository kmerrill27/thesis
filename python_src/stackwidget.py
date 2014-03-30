from defs import *
from widgetwrapper import *

class StackTopBar(QtGui.QWidget):
	""" Menu bar for stack widget label """

	def __init__(self, stack_window):
		super(StackTopBar, self).__init__()
		self.stack_window = stack_window
		self.initUI()

	def initUI(self):
		label = QtGui.QLabel()
		label.setText(STACK_WIDGET_TITLE)

		self.reverse_button = QtGui.QPushButton()
		self.reverse_button.setCheckable(True)
		self.reverse_button.setIcon(QtGui.QIcon(UP_ICON))
		self.reverse_button.setToolTip(REVERSE_BUTTON_LABEL)
		self.reverse_button.setMaximumWidth(BUTTON_WIDTH)
		self.reverse_button.toggled.connect(self.stackFlipped)

		box = QtGui.QHBoxLayout()
		box.addWidget(label)
		box.addWidget(self.reverse_button)
		self.setLayout(box)

	def stackFlipped(self, checked):
		""" Reverse stack to grow up or down """
		if checked:
			self.reverse_button.setIcon(QtGui.QIcon(DOWN_ICON))
		else:
			self.reverse_button.setIcon(QtGui.QIcon(UP_ICON))
		self.stack_window.flip(checked)

class StackWindow(QtGui.QWidget):
	""" Window for displaying call stack """

	def __init__(self, frame_widget, source_and_assembly_widget):
		super(StackWindow, self).__init__()
		self.frame_widget = frame_widget
		self.source_and_assembly_widget = source_and_assembly_widget
		self.stack = []
		self.reverse = False # True is stack growing down
		self.initUI()

	def initUI(self):
		self.stack_box = QtGui.QVBoxLayout()
		self.stack_box.setDirection(QtGui.QBoxLayout.TopToBottom)
		self.stack_box.addStretch() # This adds 1 to the count of stack_box
		self.stack_box.setSpacing(2)
		self.setLayout(self.stack_box)

		self.button_group = QtGui.QButtonGroup()
		self.button_group.buttonClicked.connect(self.frameSelected)

	def flip(self, checked):
		""" Reverse stack to grow up or down """
		self.reverse = checked
		if self.reverse:
			self.stack_box.setDirection(QtGui.QBoxLayout.BottomToTop)
		else:
			self.stack_box.setDirection(QtGui.QBoxLayout.TopToBottom)
		self.frame_widget.flip(checked)

	def frameSelected(self):
		""" Update frame display to match new frame selection """
		frame_index = self.stack_box.indexOf(self.button_group.checkedButton())
		frame_index = len(self.stack) - frame_index - 1
		self.frame_widget.displayFrame(self.stack[frame_index])
		self.source_and_assembly_widget.setLine(self.stack[frame_index].line, self.stack[frame_index].assembly)

	def pushFrame(self, frame):
		""" Add frame to top of stack """
		self.frame_widget.clearBoxes()

		frame_button = QtGui.QPushButton(frame.title)
		frame_button.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		frame_button.setCheckable(True)
		frame_button.setChecked(True)

		self.button_group.addButton(frame_button)

		self.stack_box.insertWidget(0, frame_button, 2)

		self.stack.append(frame)

		self.frameSelected()

	def popFrame(self):
		""" Remove top frame on stack """
		# Number of frames should be the same as the number of buttons in stack display
		start_length = len(self.stack)
		assert start_length == self.stack_box.count()-1

		if start_length > 1:
			self.stack.pop()

			self.removeButton(self.stack_box.itemAt(0).widget())
			self.stack_box.itemAt(0).widget().setChecked(True)

			# Select new top frame
			self.frameSelected()
			return True

		# On main frame - do not remove
		return False

	def peekFrame(self):
		""" Return top frame on stack """
		return self.stack[-1]

	def clear(self):
		""" Remove all frames from display """
		self.frame_widget.clear()
		for button in self.button_group.buttons():
			self.removeButton(button)

		for i in range (1, self.stack_box.count()): # First item is stretch - do not remove
			self.stack_box.itemAt(i).widget().close()
			self.stack_box.takeAt(i)
		self.stack = []

	def removeButton(self, button):
		""" Remove frame button from stack display """
		self.stack_box.removeWidget(button)
		self.button_group.removeButton(button)
		button.close()
