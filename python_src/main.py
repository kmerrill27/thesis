#!/usr/bin/env python

"""
StackExplorer

An interactive call stack visualization tool for novice programmers

course: CS senior project, Pomona College
name: Kim Merrill
date: March 27, 2014
advisor: Rett Bull

"""

import sys

from defs import *
from stackviz import *

class StackApp(QtGui.QMainWindow):
	""" Main PyQt application window """

	def __init__(self):
		super(StackApp, self).__init__()
		self.initUI()
		self.show()

	def initUI(self):
		stack_viz = StackVisualizer()
		self.setCentralWidget(stack_viz)
		self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
		self.setWindowTitle(APP_TITLE)
		self.setWindowIcon(QtGui.QIcon(STACK_ICON))

def main():
	app = QtGui.QApplication(sys.argv)

	stack_viz = StackApp()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
	