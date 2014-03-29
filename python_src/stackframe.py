from arch import *
from defs import *
from widgetwrapper import *

class StackFrame:
	""" Representation of a stack frame """

	def __init__(self, title, architecture, frame_ptr, stack_ptr, bottom, line, assembly):
		self.title = title # Function name
		self.architecture = architecture
		self.frame_ptr = frame_ptr
		self.stack_ptr = stack_ptr
		self.bottom = bottom # Base address of frame
		self.line = line # Current source line
		self.assembly = assembly # Current assembly instructions
		self.items = [] # Items are symbols, saved registers, etc.

	def addItem(self, frame_item):
		""" Add item to top of frame """
		self.items.insert(0, frame_item)

class FrameItem:
	""" Representation of an object (symbol, saved register, etc.) in a stack frame """

	def __init__(self):
		self.title = None
		self.addr = None
		self.length = None # Item length in bits
		self.value = None
		self.initialized = None
		self.struct = None # Symbol prefix - e.x. (struct node *) - blank if not struct
		self.zoom_val = None # Detail view - different from value only for structs

class FrameDisplay(QtGui.QTableWidget):
	""" Widget for displaying current stack frame """

	def __init__(self, frame, addr_box, inspect_on, decimal_on):
		super(FrameDisplay, self).__init__()
		self.frame = frame
		self.addr_box = addr_box
		self.inspect_on = inspect_on
		self.decimal_on = decimal_on
		self.initUI()

	def initUI(self):
		self.setColumnCount(1)
		self.horizontalHeader().hide()
		self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		self.show()
		# Set height to height of items so no whitespace
		self.setMaximumHeight(self.rowCount()*self.rowHeight(0) + 2)
		self.highlightStackPointer()

	def show(self):
		""" Display all items in stack frame """
		# Sort items in increasing address order
		sorted_list = sorted(self.frame.items, key=lambda x: x.addr)
		if self.frame.stack_ptr != None:
			# Not in main
			self.addTempStorageSpace(int(sorted_list[0].addr, 16))

		for item in sorted_list:
			self.displayItem(item)

	def displayItem(self, frame_item):
		""" Display item, which is a symbol, saved register, etc. """
		item_title = QtGui.QLabel()
		if not frame_item.initialized:
			# Symbol uninitialized
			item_title.setText(" " + frame_item.title + " =\n     " + UNINITIALIZED)
			item_title.setStatusTip(UNINITIALIZED)
		else:
			# Symbol initialized
			item_title.setText(" " + frame_item.title + " =\n     " + frame_item.struct + frame_item.value)
			item_title.setStatusTip(frame_item.zoom_val)

		row_span = int(frame_item.length)/4 # One row is 4 bytes

		for i in range(0, row_span):
			# Set item to take up number of rows corresponding to its length
			self.insertRow(self.rowCount())
			header = QtGui.QTableWidgetItem("")
			# Set tooltip to address of item
			header.setToolTip(CARAT + str(hex(int(frame_item.addr, 16) + 4*i)))
			self.setVerticalHeaderItem(self.rowCount() - 1, header)

			if i == 0:
				if self.frame.frame_ptr == frame_item.addr and self.frame.stack_ptr == frame_item.addr:
					# Frame pointer and stack pointer at address
					header.setText(self.frame.architecture.base_pointer + "/" + self.frame.architecture.stack_pointer)
				elif self.frame.frame_ptr == frame_item.addr:
					# Frame pointer only at address
					header.setText(self.frame.architecture.base_pointer)
				elif self.frame.stack_ptr == frame_item.addr:
					# Stack pointer only at address
					header.setText(self.frame.architecture.stack_pointer)

		# Add item to table
		new_row = self.rowCount() - row_span
		self.setCellWidget(new_row, 0, item_title)

		if row_span > 1:
			self.setSpan(new_row, 0, row_span, 1)

	def selectionChanged(self, selected, deselected):
		""" Frame item (row in table) selected """
		if self.inspect_on:
			self.setInspectBox()
		else:
			self.setAddressBox()

	def addTempStorageSpace(self, last_addr):
		""" Add empty temporary storage space to reach top of frame """
		# Need temp storage space if stack pointer above topmost item
		temp_space = (last_addr - int(self.frame.stack_ptr, 16)) / 4

		for i in range(0, temp_space):
			self.insertRow(self.rowCount())
			header = QtGui.QTableWidgetItem("")
			curr_addr = hex(int(self.frame.stack_ptr, 16) + 4*i)
			header.setToolTip(CARAT + str(curr_addr))
			self.setVerticalHeaderItem(self.rowCount() - 1, header)

			# Display stack pointer at its address
			if self.frame.stack_ptr == curr_addr:
				header.setText(self.frame.architecture.stack_pointer)

	def highlightStackPointer(self):
		""" Select row at stack pointer address """
		for i in range(0, self.rowCount()):
			header_text = self.verticalHeaderItem(i).text()
			if header_text and self.frame.architecture.stack_pointer in header_text:
				self.selectRow(i)

	def setAddressBox(self):
		""" Set message in box to item address """
		selected = self.selectedIndexes()

		if selected:
			row = selected[0].row()
			addr = self.verticalHeaderItem(row).toolTip()
			if self.decimal_on:
				# Display address as decimal
				addr = CARAT + str(int(str(addr.replace(CARAT, "")), 16))
				self.addr_box.setText(addr)
			else:
				# Display address as hex
				self.addr_box.setText(addr)
	
	def setInspectBox(self):
		""" Set message in box to item zoom value """
		selected = self.selectedIndexes()
		
		if selected:
			if self.inspect_on:
				row = selected[0].row()	
				item = self.cellWidget(row, 0)
				if item:
					# Display item zoom value
					self.addr_box.setText(item.statusTip())
				else:
					# No item at address
					self.addr_box.clear()
			else:
				# If inspect off, display address
				self.setAddressBox()

	def toggleDecimal(self, decimal_on):
		""" Toggle decimal mode, which displays address as hex or dec """
		self.decimal_on = decimal_on
		self.setAddressBox()

	def toggleInspect(self, inspect_on):
		""" Toggle inspect mode, which displays struct zoom values """
		self.inspect_on = inspect_on
		self.setInspectBox()
