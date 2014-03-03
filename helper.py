from PyQt4 import QtGui
from PyQt4 import QtCore

def frameWrapVert(frame, widgets):
	frame.setFrameShape(QtGui.QFrame.StyledPanel)
	box = QtGui.QVBoxLayout()

	for widget in widgets:
		box.addWidget(widget)

	frame.setLayout(box)

def frameWrapHoriz(frame, widgets):
	frame.setFrameShape(QtGui.QFrame.StyledPanel)
	box = QtGui.QHBoxLayout()

	for widget in widgets:
		box.addWidget(widget)

	frame.setLayout(box)
