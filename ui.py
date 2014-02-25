import sys
from stackviz import *

# To run: python ui.py ../fact_rec.c

class StackApp(QtGui.QMainWindow):

	def __init__(self):
		super(StackApp, self).__init__()
		self.initUI()
		self.show()

	def initUI(self):
		stack_viz = StackVisualizer()
		self.setCentralWidget(stack_viz)
		self.resize(1000, 500)

		self.setWindowTitle('Stack Viz')
		self.setWindowIcon(QtGui.QIcon('stack.png'))

def main():
	app = QtGui.QApplication(sys.argv)

	stack_viz = StackApp()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()