from widgetwrapper import *

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

	def __init__(self, frame_widget, source_and_assembly_widget):
		super(StackWindow, self).__init__()
		self.frame_widget = frame_widget
		self.source_and_assembly_widget = source_and_assembly_widget
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
		self.source_and_assembly_widget.setLine(self.stack[frame_index].line, self.stack[frame_index].assembly)

	def clear(self):
		self.frame_widget.clear()
		for button in self.button_group.buttons():
			self.removeButton(button)
		# First item is stretch - do not remove
		for i in range (1, self.stack_box.count()):
			self.stack_box.itemAt(i).widget().close()
			self.stack_box.takeAt(i)
		self.stack = []

	def getTopFrame(self):
		return self.stack[-1]

	def setToMainFrame(self):
		not_on_last_frame = True
		while (not_on_last_frame):
			not_on_last_frame = self.removeFrame()

	def addFrame(self, frame):
		self.frame_widget.clearBoxes()

		frame_button = QtGui.QPushButton(frame.title)
		frame_button.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		frame_button.setCheckable(True)
		frame_button.setChecked(True)

		self.button_group.addButton(frame_button)

		self.stack_box.insertWidget(0, frame_button, 2)

		self.stack.append(frame)

		self.frameSelected()

	def removeFrame(self):
		assert len(self.stack) == self.stack_box.count()-1

		if len(self.stack) > 1:
			# Top frame was the active frame
			self.removeButton(self.stack_box.itemAt(0).widget())
			self.stack.pop()

			self.stack_box.itemAt(0).widget().setChecked(True)
			self.frameSelected()

			return True

		# Return false if on last frame
		return False

	def removeButton(self, button):
		was_checked = button == self.button_group.checkedButton()
		self.stack_box.removeWidget(button)
		self.button_group.removeButton(button)
		button.close()

		return was_checked
