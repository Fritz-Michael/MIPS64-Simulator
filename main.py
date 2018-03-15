from PyQt5 import QtWidgets, QtCore, Qt
import sys

class MainWindow(QtWidgets.QMainWindow):

	def __init__(self,parent=None):
		super(MainWindow, self).__init__(parent)
		self.resize(1366,768)
		self.widget_frame = WindowFrame(Tabs)
		self.setCentralWidget(self.widget_frame)


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
		self.frame = frame
		self.init_ui()

	def init_ui(self):
		self.input_label = QtWidgets.QLabel("Input")
		self.addWidget(self.input_label, 1, 1, 1, 1)


class OpcodeView(QtWidgets.QGridLayout):

	def __init__(self,frame):
		super().__init__()
		self.frame = frame

	def init_ui(self):
		self.opcode_label = QtWidgets.QLabel("Opcode")
		self.addWidget(self.opcode_label, 1, 1, 1, 1)


class MemoryAndRegisterView(QtWidgets.QGridLayout):

	def __init__(self,frame):
		super().__init__()
		self.frame = frame

	def init_ui(self):
		self.memory_label = QtWidgets.QLabel("Memory and register")
		self.addWidget(self.memory_label, 1, 1, 1, 1)


class PipelineMapView(QtWidgets.QGridLayout):

	def __init__(self,frame):
		super().__init__()
		self.frame = frame

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