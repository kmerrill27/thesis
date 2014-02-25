from PyQt4 import QtGui
from PyQt4 import QtCore

def frameWrap(top_widget, central_widget):
	self.setFrameShape(QtGui.QFrame.StyledPanel)
	box = QtGui.QVBoxLayout()
	box.addWidget(self.top_widget)
	box.addWidget(self.central_widget)
	self.setLayout(box)
