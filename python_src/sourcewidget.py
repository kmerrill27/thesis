import platform
from defs import *
from gdbstream import *
from parse import *
from stackandframewidget import *
from helper import *
from runstate import *

class SourceWidget(QtGui.QFrame):

	def __init__(self, assembly_widget):
		super(SourceWidget, self).__init__()
		self.assembly_widget = assembly_widget
		self.initUI()

	def initUI(self):
		self.window = SourceWindow()
		self.top_bar = SourceTopBar(self.assembly_widget, self.window)
		frameWrapVert(self, [self.top_bar, self.window])

	def setStackAndFrameWidget(self, stack_and_frame_widget):
		self.top_bar.setStackAndFrameWidget(stack_and_frame_widget)

	def highlightLine(self, line_num):
		self.window.highlightLine(int(line_num))

	def clear(self):
		self.window.unhighlightLines()

class SourceTopBar(QtGui.QWidget):

	def __init__(self, assembly_widget, source_window):
		super(SourceTopBar, self).__init__()
		self.assembly_widget = assembly_widget
		self.source_window = source_window
		self.stack_and_frame_widget = None
		self.initUI()

	def initUI(self):
		label = QtGui.QLabel()
		label.setText("Source Code")

		self.current_file = QtGui.QLabel()
		self.current_file.setText("No source file")

		file_button = QtGui.QPushButton("Load source")
		file_button.clicked.connect(self.fileButtonClicked)

		box = QtGui.QHBoxLayout()
		box.addWidget(label)
		box.addWidget(self.current_file)
		box.addWidget(file_button)
		self.setLayout(box)

	def setStackAndFrameWidget(self, stack_and_frame_widget):
		self.stack_and_frame_widget = stack_and_frame_widget

	def fileButtonClicked(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, "Select a C program")
		if filename:
			self.current_file.setText(os.path.basename(str(filename)))
			err = self.source_window.loadSource(str(filename))
			self.assembly_widget.clear()
			self.stack_and_frame_widget.reset()

			if (err > 0):
				self.prepareVis(str(filename))

	def prepareVis(self, filename):
		if (filename):
			command = C_COMPILE.format(self.formatPath(filename), C_OUT)
			os.system(command)

	def formatPath(self, filename):
		if (platform.system() == "Windows"):
			return filename.replace(" ", "%")
		else:
			# Unix
			return filename.replace(" ", "\ ").replace("'", "\'")

class SourceWindow(QtGui.QListWidget):

	def __init__(self):
		super(SourceWindow, self).__init__()
		self.isSource = False

	def loadSource(self, filename):
		self.clear()

		if (self.isCSource(filename)):
			with open(filename) as f:
				source_lines = [line.rstrip('\n') for line in f]
			self.addItems(source_lines)
			self.unhighlightLines()
			self.isSource = True
			return 1
		else:
			self.addItem(NOT_C_SOURCE)
			self.isSource = False
			return -1

	def highlightLine(self, line_num):
		self.setCurrentRow(line_num-1)
		self.scrollToItem(self.item(line_num-1))

	def unhighlightLines(self):
		self.setCurrentRow(-1)
		self.scrollToItem(self.item(0))

	def isCSource(self, filename):
		base_file = os.path.basename(filename)
		return base_file.endswith(".C") or base_file.endswith(".c")

	# Override to disallow user from selecting line
	def keyPressEvent(self, event):
		return

	# Override to disallow user from selecting line
	def mousePressEvent(self, event):
		return

	# Override to disallow user from selecting line
	def mouseMoveEvent(self, event):
		return
