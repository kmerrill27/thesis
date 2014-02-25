from PyQt4 import QtGui
from PyQt4 import QtCore

def frameWrap(self, top_widget, central_widget):
	self.setFrameShape(QtGui.QFrame.StyledPanel)
	box = QtGui.QVBoxLayout()
	box.addWidget(top_widget)
	box.addWidget(central_widget)
	self.setLayout(box)
