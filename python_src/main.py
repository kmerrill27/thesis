import sys
from defs import *
from stackviz import *

class StackApp(QtGui.QMainWindow):

	def __init__(self):
		super(StackApp, self).__init__()
		self.initUI()
		self.show()

	def initUI(self):
		stack_viz = StackVisualizer()
		self.setCentralWidget(stack_viz)
		self.resize(1000, 600)

		self.setWindowTitle(TITLE)
		self.setWindowIcon(QtGui.QIcon(STACK_ICON))

def main():
	app = QtGui.QApplication(sys.argv)

	stack_viz = StackApp()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()