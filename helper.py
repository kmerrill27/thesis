from PyQt4 import QtGui
from PyQt4 import QtCore

def frameWrapVert(frame, top_widget, central_widget):
	frame.setFrameShape(QtGui.QFrame.StyledPanel)
	box = QtGui.QVBoxLayout()
	box.addWidget(top_widget)
	box.addWidget(central_widget)
	frame.setLayout(box)

def frameWrapHoriz(frame, left_widget, right_widget):
	frame.setFrameShape(QtGui.QFrame.StyledPanel)
	box = QtGui.QHBoxLayout()
	box.addWidget(left_widget)
	box.addWidget(right_widget)
	frame.setLayout(box)
