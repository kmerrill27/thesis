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
		self.selected_row = 0 # Item selected

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

	def __init__(self, frame, addr_box, mode, reverse):
		super(FrameDisplay, self).__init__()
		self.frame = frame
		self.addr_box = addr_box
		self.mode = mode
		self.reverse = reverse
		self.initUI()

	def initUI(self):
		self.setColumnCount(1)
		self.horizontalHeader().hide()
		self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		if self.reverse:
			self.showReverse()
		else:
			self.show()
		# Set height to height of items so no whitespace
		self.setMaximumHeight(self.rowCount() * self.rowHeight(0) + 2)

	def show(self):
		""" Display all items in stack frame from highest to lowest address """
		last_addr = None
		# Sort items in increasing address order
		sorted_list = sorted(self.frame.items, key=lambda x: x.addr)

		if self.frame.stack_ptr != None:
			# Not in main - add empty space between top item and stack pointer
			self.addTempStorageSpace(int(sorted_list[0].addr, 16), int(self.frame.stack_ptr, 16))

		for item in sorted_list:
			item_addr = int(item.addr, 16)
			if last_addr and last_addr < item_addr:
				# Add any empty space between items
				self.addTempStorageSpace(item_addr, last_addr)

			last_addr = self.displayItem(item) + 4

		self.selectRow(self.frame.selected_row)

	def showReverse(self):
		""" Display all items in stack frame from lowest to highest address """
		last_addr = None
		# Sort items in decreasing address order
		sorted_list = sorted(self.frame.items, key=lambda x: x.addr, reverse=True)

		for item in sorted_list:
			item_addr = int(item.addr, 16)
			if last_addr and last_addr > item_addr + int(item.length):
				# Add any empty space between items
				self.addTempStorageSpace(last_addr, item_addr + int(item.length))

			last_addr = self.displayItem(item)

		if self.frame.stack_ptr != None:
			# Not in main - add empty space between top item and stack pointer
			self.addTempStorageSpace(int(sorted_list[-1].addr, 16), int(self.frame.stack_ptr, 16))

		self.selectRow(self.frame.selected_row)

	def displayItem(self, frame_item):
		""" Display item, which is a symbol, saved register, etc. """
		last_addr = -1
		item_title = self.populateItem(frame_item)
		row_span = int(frame_item.length)/4

		if self.reverse:
			offset = row_span - 1
			caret = DOWN_CARET
		else:
			offset = 0
			caret = CARET

		for i in range(0, row_span):
			self.insertRow(self.rowCount())
			last_addr = hex(int(frame_item.addr, 16) + 4 * abs(offset - i))
			header = QtGui.QTableWidgetItem(HEADER_BLANK) # Add blank space to give header width
			header.setToolTip(caret + str(last_addr))
			self.setVerticalHeaderItem(self.rowCount() - 1, header)

			if i == offset:
				self.displayPointers(frame_item.addr, header)

		self.setUpSpan(row_span, item_title)

		return int(last_addr, 16)

	def selectionChanged(self, selected, deselected):
		""" Frame item (row in table) selected """
		selections = selected.indexes()
		if selections:
			if self.reverse:
				# Lowest addressed header item corresponds to spanning item
				self.frame.selected_row = selections[-1].row()
			else:
				self.frame.selected_row = selections[0].row()

			self.setBox()

	def populateItem(self, frame_item):
		""" Set up name and value display for item """
		item_title = QtGui.QLabel()

		if not frame_item.initialized:
			# Symbol uninitialized
			item_title.setText(" " + frame_item.title + " =\n     " + UNINITIALIZED)
			item_title.setStatusTip(UNINITIALIZED)
		else:
			# Symbol initialized
			item_title.setText(" " + frame_item.title + " =\n     " + frame_item.struct + frame_item.value)
			item_title.setStatusTip(frame_item.zoom_val)

		return item_title

	def displayPointers(self, addr, header):
		""" Display frame and base pointer markers at their respective addresses """
		if self.frame.frame_ptr == addr and self.frame.stack_ptr == addr:
			# Frame pointer and stack pointer at address
			header.setText(self.frame.architecture.base_pointer + "/" + self.frame.architecture.stack_pointer)
		elif self.frame.frame_ptr == addr:
			# Frame pointer only at address
			header.setText(self.frame.architecture.base_pointer)
		elif self.frame.stack_ptr == addr:
			# Stack pointer only at address
			header.setText(self.frame.architecture.stack_pointer)		

	def setUpSpan(self, row_span, item_title):
		""" Set up item to span number of rows proptional to its length """
		new_row = self.rowCount() - row_span
		self.setCellWidget(new_row, 0, item_title)

		if row_span > 1:
			new_row = self.rowCount() - row_span
			self.setSpan(new_row, 0, row_span, 1)

	def addTempStorageSpace(self, high_addr, low_addr):
		""" Add empty temporary storage space to reach top of frame """
		# Need temp storage space if stack pointer above topmost item
		temp_space = (high_addr - low_addr) / 4

		for i in range(0, temp_space):
			self.insertRow(self.rowCount())
			header = QtGui.QTableWidgetItem("")
			self.setVerticalHeaderItem(self.rowCount() - 1, header)

			if self.reverse:
				curr_addr = hex(low_addr + 4 * (temp_space - 1 - i))
				header.setToolTip(DOWN_CARET + str(curr_addr))
			else:
				curr_addr = hex(low_addr + 4 * i)
				header.setToolTip(CARET + str(curr_addr))

			# Display stack pointer at its address
			if self.frame.stack_ptr == curr_addr:
				header.setText(self.frame.architecture.stack_pointer)

	def setBox(self):
		""" Set address box to item element according to current mode """
		if self.mode == ZOOM_MODE:
			for i in range(0, self.rowSpan(self.frame.selected_row, 0)):
				# Find row with widget in span
				item = self.cellWidget(self.frame.selected_row - i, 0)

				if item:
					# Display item zoom value
					self.addr_box.setText(item.statusTip())
					return
			
			# No item at address
			self.addr_box.clear()
		else:
			addr = self.verticalHeaderItem(self.frame.selected_row).toolTip()
			if self.mode == DECIMAL_MODE:
				if self.reverse:
					addr = DOWN_CARET + str(int(str(addr.replace(DOWN_CARET, "")), 16))
				else:
					addr = CARET + str(int(str(addr.replace(CARET, "")), 16))
			self.addr_box.setText(addr)

	def setMode(self, mode):
		""" Set display mode to hexadecimal, decimal, or zoom value """
		self.mode = mode
		self.setBox()
