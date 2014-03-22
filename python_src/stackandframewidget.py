from stackframe import *
from stackwidget import *
from framewidget import *

class StackAndFrameWidget(QtGui.QFrame):

	def __init__(self, gdb_process, source_and_assembly_widget):
		super(StackAndFrameWidget, self).__init__()
		self.gdb_process = gdb_process
		self.source_and_assembly_widget = source_and_assembly_widget
		self.initUI()

	def initUI(self):
		self.frame_widget = FrameWidget()

		self.top_bar = StackTopBar()
		self.stack_widget = StackWindow(self.frame_widget, self.source_and_assembly_widget)
		self.stack_widget_frame = QtGui.QFrame()

		frameWrapVert(self.stack_widget_frame, [self.top_bar, self.stack_widget])
		wrapHoriz(self, [self.stack_widget_frame, self.frame_widget])

	def addFrame(self, frame):
		self.stack_widget.addFrame(frame)

	def removeFrame(self):
		frame = self.stack_widget.removeFrame()

	def clear(self):
		self.stack_widget.clear()
		self.gdb_process.gdbReset()

	def getCurrentFrame(self):
		return self.frame_widget.getCurrentFrame()
