from helper import *

class StackTopBar(QtGui.QWidget):

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

	def __init__(self, frame_widget):
		super(StackWindow, self).__init__()
		self.frame_widget = frame_widget
		self.stack = []
		self.initUI()

	def initUI(self):
		self.stack_box = QtGui.QVBoxLayout()
		# This adds 1 to the count of stack_box
		self.stack_box.addStretch()
		self.stack_box.setSpacing(2)
		self.setLayout(self.stack_box)

		self.button_group = QtGui.QButtonGroup()
		self.button_group.buttonClicked.connect(self.frameSelected)

	def frameSelected(self):
		frame_index = self.stack_box.indexOf(self.button_group.checkedButton())
		frame_index = len(self.stack) - frame_index - 1
		self.frame_widget.displayFrame(self.stack[frame_index])

	def clear(self):
		for button in self.button_group.buttons():
			self.removeButton(button)
		self.stack = []

	def addFrame(self, frame):
		frame_button = QtGui.QPushButton(frame.title)
		frame_button.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		frame_button.setCheckable(True)
		frame_button.setChecked(True)

		self.button_group.addButton(frame_button)

		self.stack_box.insertWidget(0, frame_button, 2)

		self.stack.append(frame)

	def removeFrame(self):
		assert len(self.stack) == self.stack_box.count()-1

		if len(self.stack) > 0:
			# Top frame was the active frame
			was_checked = self.removeButton(self.stack_box.itemAt(0).widget())
			self.stack.pop()

			# If active frame was the one removed, make top frame active frame
			if len(self.stack) > 0 and was_checked:
				self.stack_box.itemAt(0).widget().setChecked(True)
				self.frameSelected()

	def removeButton(self, button):
		was_checked = button == self.button_group.checkedButton()
		self.stack_box.removeWidget(button)
		self.button_group.removeButton(button)
		button.close()

		return was_checked
