from framewidget import *
from stackframe import *
from stackwidget import *

class StackAndFrameWidget(QtGui.QFrame):
	""" Widget for displaying call stack and current stack frame """

	def __init__(self, source_and_assembly_widget):
		super(StackAndFrameWidget, self).__init__()
		self.source_and_assembly_widget = source_and_assembly_widget
		self.initUI()

	def initUI(self):
		self.frame_widget = FrameWidget()

		self.top_bar = StackTopBar()
		self.stack_widget = StackWindow(self.frame_widget, self.source_and_assembly_widget)
		self.stack_widget_frame = QtGui.QFrame()

		frameWrapVert(self.stack_widget_frame, [self.top_bar, self.stack_widget])
		wrapHoriz(self, [self.stack_widget_frame, self.frame_widget])

	def pushFrame(self, frame):
		""" Add frame to top of stack """
		self.stack_widget.pushFrame(frame)

	def popFrame(self):
		""" Remove top frame on stack """
		return self.stack_widget.popFrame()

	def peekFrame(self):
		""" Return top frame on stack """
		return self.stack_widget.peekFrame()

	def updateTopFrame(self, frame):
		""" Update top stack frame """
		self.frame_widget.displayFrame(frame)

	def returned(self, retval):
		""" Display retval and pop frame on return from a function call """
		self.frame_widget.returned(retval)
		self.popFrame()

	def finish(self, exit_status, frame):
		""" Show final frame display on program exit """ 
		self.frame_widget.finish(exit_status, frame)

	def clear(self):
		""" Clear stack and frame display """
		self.stack_widget.clear()
		self.frame_widget.clear()

	def toggleDecimal(self, decimal_on):
		""" Toggle decimal mode, which displays address as hex or dec """
		self.frame_widget.toggleDecimal(decimal_on)

	def toggleInspect(self, inspect_on):
		""" Toggle inspect mode, which displays struct zoom values """
		self.frame_widget.toggleInspect(inspect_on)
