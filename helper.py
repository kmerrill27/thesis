from PyQt4 import QtGui
from PyQt4 import QtCore

def frameWrapVert(frame, widgets):
	frame.setFrameShape(QtGui.QFrame.StyledPanel)
	wrapVert(frame, widgets)

def frameWrapHoriz(frame, widgets):
	frame.setFrameShape(QtGui.QFrame.StyledPanel)
	wrapHoriz(frame, widgets)

def wrapVert(frame, widgets):
	box = QtGui.QVBoxLayout()

	for widget in widgets:
		box.addWidget(widget)

	frame.setLayout(box)

def wrapHoriz(frame, widgets):
	box = QtGui.QHBoxLayout()

	for widget in widgets:
		box.addWidget(widget)

	frame.setLayout(box)

def splitterWrapVert(layout, widgets):
	splitter = QtGui.QSplitter(QtCore.Qt.Vertical)

	for widget in widgets:
		splitter.addWidget(widget)

	layout.addWidget(splitter)

def splitterWrapHoriz(layout, widgets):
	splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)

	for widget in widgets:
		splitter.addWidget(widget)

	layout.addWidget(splitter)
