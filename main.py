from PyQt5 import QtWidgets, QtCore
import sys
import os
from modules import *
from modules.instructions import *
from modules.pipelinemap import *

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
        self.instruction_opcode = []
        self.text = QtWidgets.QPlainTextEdit()
        self.load = QtWidgets.QPushButton("Load")
        self.reset = QtWidgets.QPushButton("Reset")
        self.instructions = []
        # self.singleStep = QtWidgets.QPushButton("Single Step Execute")
        # self.fullExec = QtWidgets.QPushButton("Full Execute")
        self.pipeline = Pipeline([''])
        self.init_ui()

    def init_ui(self):
        #self.input_label = QtWidgets.QLabel("Input")
        self.addWidget(self.text, 0, 0, 1, 2)
        self.addWidget(self.load, 1, 0, 1, 1)
        self.addWidget(self.reset, 1, 1, 1, 1)
        # self.addWidget(self.singleStep, 2, 0, 1, 1)
        # self.addWidget(self.fullExec, 2, 1, 1, 1)
        self.load.clicked.connect(self.load_input)

    @QtCore.pyqtSlot()
    def load_input(self):
        textInput = str(self.text.toPlainText())
        self.instructions = textInput.splitlines()
        self.opcode = Opcode(self.instructions)
        print(self.instructions)

        try:
            self.instruction_opcode = list(map(lambda x: self.opcode.get_opcode(x),self.instructions))
            self.pipeline = Pipeline(self.instruction_opcode)
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print(e)

    def reset_registers(self):
        try:
            self.pipeline.internal_registers.__init__(self.instruction_opcode)
        except:
            pass

class OutputView(QtWidgets.QGridLayout):

    def __init__(self,frame):
        super().__init__()
        self.frame = frame
        self.instructionTable = QtWidgets.QTableWidget()
        self.instructionScroll = QtWidgets.QScrollArea()
        self.pipelineTable = QtWidgets.QTableWidget()
        self.pipelineScroll = QtWidgets.QScrollArea()
        self.memoryScroll = QtWidgets.QScrollArea()
        self.memoryTable = QtWidgets.QTableWidget()
        self.gpRegisterScroll = QtWidgets.QScrollArea()
        self.gpRegisterTable = QtWidgets.QTableWidget()

        self.pipeline = Pipeline([''])

        self.latestRow = 0
        self.gp_registers_label = QtWidgets.QLabel("GP Registers")
        self.opcode_label = QtWidgets.QLabel("Opcode")
        self.mem_label = QtWidgets.QLabel("Memory")
        self.pipelineLabel = QtWidgets.QLabel("Pipeline Map")
        self.init_ui()

    def init_ui(self):

        #Change row count to instruction count
        self.instructionTable.setColumnCount(8)
        self.instructionTable.setHorizontalHeaderItem(0,QtWidgets.QTableWidgetItem("Instructions"))
        self.instructionTable.setHorizontalHeaderItem(1,QtWidgets.QTableWidgetItem("B: 31-26"))
        self.instructionTable.setHorizontalHeaderItem(2,QtWidgets.QTableWidgetItem("B: 25-21"))
        self.instructionTable.setHorizontalHeaderItem(3,QtWidgets.QTableWidgetItem("B: 20-16"))
        self.instructionTable.setHorizontalHeaderItem(4,QtWidgets.QTableWidgetItem("B: 15-11"))
        self.instructionTable.setHorizontalHeaderItem(5,QtWidgets.QTableWidgetItem("B: 10-6"))
        self.instructionTable.setHorizontalHeaderItem(6,QtWidgets.QTableWidgetItem("B: 5-0"))
        self.instructionTable.setHorizontalHeaderItem(7,QtWidgets.QTableWidgetItem("HEX"))
        self.instructionScroll.setWidget(self.instructionTable)
        self.instructionScroll.setWidgetResizable(True)
        self.addWidget(self.opcode_label, 0, 0, 1, 1)
        self.addWidget(self.instructionScroll, 1, 0, 1, 1)

        self.pipelineTable.setColumnCount(1)
        self.pipelineTable.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Instructions"))
        self.pipelineScroll.setWidget(self.pipelineTable)
        self.pipelineScroll.setWidgetResizable(True)
        self.addWidget(self.pipelineLabel, 2, 0, 1, 1)
        self.addWidget(self.pipelineScroll, 3, 0, 1, 1)

        self.gpRegisterTable.setColumnCount(2)
        self.gpRegisterTable.setHorizontalHeaderItem(0,QtWidgets.QTableWidgetItem("GP Registers"))
        self.gpRegisterTable.setHorizontalHeaderItem(1,QtWidgets.QTableWidgetItem("Value"))
        self.gpRegisterTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.gpRegisterTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.gpRegisterScroll.setWidget(self.gpRegisterTable)
        self.gpRegisterScroll.setWidgetResizable(True)
        self.addWidget(self.gp_registers_label, 0, 1, 1, 1)
        self.addWidget(self.gpRegisterScroll, 1, 1, 1, 1)

        self.memoryTable.setColumnCount(2)
        self.memoryTable.setHorizontalHeaderItem(0,QtWidgets.QTableWidgetItem("Memory"))
        self.memoryTable.setHorizontalHeaderItem(1,QtWidgets.QTableWidgetItem("Value"))
        self.memoryTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.memoryTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.memoryScroll.setWidget(self.memoryTable)
        self.memoryScroll.setWidgetResizable(True)
        self.addWidget(self.mem_label, 2, 1, 1, 1)
        self.addWidget(self.memoryScroll, 3, 1, 1, 1)

    def get_pipeline(self, pipeline):
        self.pipeline = pipeline


# class MemoryAndRegisterView(QtWidgets.QGridLayout):
#
# 	def __init__(self,frame):
# 		super().__init__()
# 		self.frame = frame
# 		self.init_ui()
#
# 	def init_ui(self):
# 		self.memory_label = QtWidgets.QLabel("Memory and register")
# 		self.addWidget(self.memory_label, 1, 1, 1, 1)
#
#
# class PipelineMapView(QtWidgets.QGridLayout):
#
# 	def __init__(self,frame):
# 		super().__init__()
# 		self.frame = frame
# 		self.init_ui()
#
# 	def init_ui(self):
# 		self.pipeline_label = QtWidgets.QLabel("Pipeline")
# 		self.addWidget(self.pipeline_label, 1, 1, 1, 1)



class Tabs(QtWidgets.QGridLayout):

    def __init__(self,parent=None):
        super(QtWidgets.QGridLayout, self).__init__(parent)
        self.tabs = QtWidgets.QTabWidget()
        self.input_tabs = WindowFrame(InputView)

        self.output_tabs = WindowFrame(OutputView)
        self.tabs.addTab(self.input_tabs,"Input")
        self.tabs.addTab(self.output_tabs,"Output")
        self.addWidget(self.tabs)
        self.tabs.currentChanged.connect(self.pass_pipeline)
    def pass_pipeline(self):
        self.output_tabs.layout.get_pipeline(self.input_tabs.layout.pipeline)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
