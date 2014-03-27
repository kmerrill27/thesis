from PyQt4 import QtCore
from PyQt4 import QtGui

def frameWrapVert(frame, widgets):
	""" Vertically wraps list of widgets in bordered frame """
	frame.setFrameShape(QtGui.QFrame.StyledPanel)
	wrapVert(frame, widgets)

def frameWrapHoriz(frame, widgets):
	""" Horizontally wraps list of widgets in bordered frame """
	frame.setFrameShape(QtGui.QFrame.StyledPanel)
	wrapHoriz(frame, widgets)

def wrapVert(frame, widgets):
	""" Vertically wraps list of widgets """
	box = QtGui.QVBoxLayout()

	for widget in widgets:
		box.addWidget(widget)

	frame.setLayout(box)

def wrapHoriz(frame, widgets):
	""" Horizontally wraps list of widgets """
	box = QtGui.QHBoxLayout()

	for widget in widgets:
		box.addWidget(widget)

	frame.setLayout(box)

def splitterWrapVert(layout, widgets):
	""" Vertically wraps list of widgets in resizable splitter """
	splitter = QtGui.QSplitter(QtCore.Qt.Vertical)

	for widget in widgets:
		splitter.addWidget(widget)

	layout.addWidget(splitter)

def splitterWrapHoriz(layout, widgets):
	""" Horizontally wraps list of widgets in resizable splitter """
	splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)

	for widget in widgets:
		splitter.addWidget(widget)

	layout.addWidget(splitter)
