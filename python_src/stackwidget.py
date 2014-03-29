from widgetwrapper import *

class StackTopBar(QtGui.QWidget):
	""" Menu bar for stack widget label """

	def __init__(self):
		super(StackTopBar, self).__init__()
		self.initUI()

	def initUI(self):
		label = QtGui.QLabel()
		label.setText("Call Stack")

		box = QtGui.QHBoxLayout()
		box.addWidget(label)
		self.setLayout(box)

class StackWindow(QtGui.QWidget):
	""" Window for displaying call stack """

	def __init__(self, frame_widget, source_and_assembly_widget):
		super(StackWindow, self).__init__()
		self.frame_widget = frame_widget
		self.source_and_assembly_widget = source_and_assembly_widget
		self.stack = []
		self.initUI()

	def initUI(self):
		self.stack_box = QtGui.QVBoxLayout()
		self.stack_box.addStretch() # This adds 1 to the count of stack_box
		self.stack_box.setSpacing(2)
		self.setLayout(self.stack_box)

		self.button_group = QtGui.QButtonGroup()
		self.button_group.buttonClicked.connect(self.frameSelected)

	def frameSelected(self):
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
		assert len(self.stack) == self.stack_box.count()-1

		if len(self.stack) > 1:
			self.removeButton(self.stack_box.itemAt(0).widget())
			self.stack.pop()

			# Select new top frame
			self.stack_box.itemAt(0).widget().setChecked(True)
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
