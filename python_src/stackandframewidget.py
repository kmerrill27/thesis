from framewidget import *
from stackframe import *
from stackwidget import *

class StackAndFrameWidget(QtGui.QFrame):

	def __init__(self, gdb_process, source_and_assembly_widget):
		super(StackAndFrameWidget, self).__init__()
		self.gdb_process = gdb_process
		self.source_and_assembly_widget = source_and_assembly_widget
		self.finished = False
		self.initUI()

	def initUI(self):
		self.frame_widget = FrameWidget()

		self.top_bar = StackTopBar()
		self.stack_widget = StackWindow(self.frame_widget, self.source_and_assembly_widget)
		self.stack_widget_frame = QtGui.QFrame()

		frameWrapVert(self.stack_widget_frame, [self.top_bar, self.stack_widget])
		wrapHoriz(self, [self.stack_widget_frame, self.frame_widget])

	def updateFrame(self, frame):
		self.frame_widget.displayFrame(frame)
		self.source_and_assembly_widget.setLine(frame.line, frame.assembly)

	def addFrame(self, frame):
		self.stack_widget.addFrame(frame)
		self.source_and_assembly_widget.setLine(frame.line, frame.assembly)

	def removeFrame(self):
		return self.stack_widget.removeFrame()

	def returned(self, retval):
		self.frame_widget.returned(retval)
		self.removeFrame()

	def finish(self, exit_status, frame):
		self.frame_widget.finish(exit_status, frame)
		self.finished = True

	def clear(self):
		self.stack_widget.clear()
		self.frame_widget.clear()

	def reset(self):
		self.clear()
		self.gdb_process.gdbReset()
		self.finished = False

	def toggleDecimal(self, decimal_on):
		self.frame_widget.toggleDecimal(decimal_on)

	def toggleInspect(self, inspect_on):
		self.frame_widget.toggleInspect(inspect_on)

	def getTopFrame(self):
		return self.stack_widget.getTopFrame()
