from PyQt5 import QtWidgets, QtCore, Qt
import sys
import os

class MainWindow(QtWidgets.QMainWindow):

	def __init__(self,parent=None):
		super(MainWindow, self).__init__(parent)
		super().setWindowTitle("microMips Simulator")
		self.resize(1280,720)

		menuBar = self.menuBar()
		fileMenu = menuBar.addMenu('File')
		editMenu = menuBar.addMenu('Edit')
		viewMenu = menuBar.addMenu('View')
		runMenu = menuBar.addMenu('Run')
		helpMenu = menuBar.addMenu('Help')

		#Add submenus
		save_action = QtWidgets.QAction('Save', self)
		open_action = QtWidgets.QAction('Open', self)
		oneCyc_action = QtWidgets.QAction('Execute 1 cycle', self)
		fullCyc_action = QtWidgets.QAction('Execute all possible cycles', self)

		#Link functions to action
		save_action.triggered.connect(self.save_text)
		open_action.triggered.connect(self.open_text)

		#Add actions to fileMenu
		fileMenu.addAction(open_action)
		fileMenu.addAction(save_action)
		runMenu.addAction(oneCyc_action)
		runMenu.addAction(fullCyc_action)

		self.widget_frame = WindowFrame(Tabs)
		self.setCentralWidget(self.widget_frame)


	def save_text(self):
		filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'))
		with open(filename[0], 'w') as f:
			my_text = main.widget_frame.layout.input_tabs.layout.text.toPlainText()
			f.write(my_text)

	def open_text(self):
		filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
		with open(filename[0], 'r') as f:
			file_text = f.read()
			main.widget_frame.layout.input_tabs.layout.text.clear()
			main.widget_frame.layout.input_tabs.layout.text.insertPlainText(file_text)

	def clear_text(self):
		self.text.clear()

class WindowFrame(QtWidgets.QWidget):

	def __init__(self,layout,extra=None):
		super().__init__()
		if extra is None:
			self.layout = layout(self)
		else:
			self.layout = layout(self,extra)
		self.setLayout(self.layout)

class InputView(QtWidgets.QGridLayout):

	def __init__(self,frame):
		super().__init__()
		self.text = QtWidgets.QPlainTextEdit()
		self.load = QtWidgets.QPushButton("Load")
		self.reset = QtWidgets.QPushButton("Reset")
		self.init_ui()

	def init_ui(self):
		#self.input_label = QtWidgets.QLabel("Input")
		self.addWidget(self.text, 0, 0, 1, 2)
		self.addWidget(self.load, 1, 0, 1, 1)
		self.addWidget(self.reset, 1, 1, 1, 1)

class OpcodeView(QtWidgets.QGridLayout):

	def __init__(self,frame):
		super().__init__()
		self.frame = frame
		self.instructionTable = QtWidgets.QTableWidget()
		self.latestRow = 0
		self.init_ui()

	def init_ui(self):
		self.opcode_label = QtWidgets.QLabel("Opcode")
		#Change row count to instruction count
		self.instructionTable.setRowCount(5)
		self.instructionTable.setColumnCount(8)
		self.instructionTable.setItem(0,0,QtWidgets.QTableWidgetItem("Instructions"))
		self.instructionTable.setItem(0,1,QtWidgets.QTableWidgetItem("B: 31-26"))
		self.instructionTable.setItem(0,2,QtWidgets.QTableWidgetItem("B: 25-21"))
		self.instructionTable.setItem(0,3,QtWidgets.QTableWidgetItem("B: 20-16"))
		self.instructionTable.setItem(0,4,QtWidgets.QTableWidgetItem("B: 15-11"))
		self.instructionTable.setItem(0,5,QtWidgets.QTableWidgetItem("B: 10-6"))
		self.instructionTable.setItem(0,6,QtWidgets.QTableWidgetItem("B: 5-0"))
		self.instructionTable.setItem(0,7,QtWidgets.QTableWidgetItem("HEX"))
		self.addWidget(self.instructionTable, 1, 1, 1, 1)


class MemoryAndRegisterView(QtWidgets.QGridLayout):

	def __init__(self,frame):
		super().__init__()
		self.frame = frame
		self.init_ui()

	def init_ui(self):
		self.memory_label = QtWidgets.QLabel("Memory and register")
		self.addWidget(self.memory_label, 1, 1, 1, 1)


class PipelineMapView(QtWidgets.QGridLayout):

	def __init__(self,frame):
		super().__init__()
		self.frame = frame
		self.init_ui()

	def init_ui(self):
		self.pipeline_label = QtWidgets.QLabel("Pipeline")
		self.addWidget(self.pipeline_label, 1, 1, 1, 1)


class Tabs(QtWidgets.QGridLayout):

	def __init__(self,parent=None):
		super(QtWidgets.QGridLayout, self).__init__(parent)
		self.tabs = QtWidgets.QTabWidget()
		self.input_tabs = WindowFrame(InputView)
		self.opcode_tabs = WindowFrame(OpcodeView)
		self.memory_tabs = WindowFrame(MemoryAndRegisterView)
		self.pipeline_tabs = WindowFrame(PipelineMapView)
		self.tabs.addTab(self.input_tabs,"Input")
		self.tabs.addTab(self.opcode_tabs,"Opcode")
		self.tabs.addTab(self.memory_tabs,"Memory and Registers")
		self.tabs.addTab(self.pipeline_tabs,"Pipeline Map")
		self.addWidget(self.tabs)


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())
