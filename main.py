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

        update_action = QtWidgets.QAction('Update output', self)
        oneCyc_action = QtWidgets.QAction('Execute 1 cycle', self)
        fullCyc_action = QtWidgets.QAction('Execute all possible cycles', self)

        #Link functions to action
        save_action.triggered.connect(self.save_text)
        open_action.triggered.connect(self.open_text)
        oneCyc_action.triggered.connect(self.run_one_cyc)
        fullCyc_action.triggered.connect(self.full_exec)
        #Add actions to fileMenu
        fileMenu.addAction(open_action)
        fileMenu.addAction(save_action)
        runMenu.addAction(oneCyc_action)
        runMenu.addAction(fullCyc_action)
        runMenu.addAction(update_action)
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

    def update_output(self):
        main.widget_frame.layout.output_tabs.layout.update_opcode()

    def run_one_cyc(self):
        main.widget_frame.layout.output_tabs.layout.cycleCtr+=1
        main.widget_frame.layout.output_tabs.layout.updatePipeline()
        main.widget_frame.layout.output_tabs.layout.updateRegisterValues()
        main.widget_frame.layout.output_tabs.layout.updateMemory()

    def full_exec(self):
        main.widget_frame.layout.output_tabs.layout.cycleCtr=len(main.widget_frame.layout.output_tabs.layout.pipeline.values)-1
        main.widget_frame.layout.output_tabs.layout.updatePipeline()
        main.widget_frame.layout.output_tabs.layout.updateRegisterValues()
        main.widget_frame.layout.output_tabs.layout.updateMemory()
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
        self.frame = frame
        self.instruction_opcode = []
        self.text = QtWidgets.QPlainTextEdit()
        self.load = QtWidgets.QPushButton("Load")
        self.reset = QtWidgets.QPushButton("Reset")
        self.instructions = []
        self.instruction_opcode = []
        # self.singleStep = QtWidgets.QPushButton("Single Step Execute")
        # self.fullExec = QtWidgets.QPushButton("Full Execute")
        self.pipeline = Pipeline([''],[''])
        self.init_ui()

    def init_ui(self):
        #self.input_label = QtWidgets.QLabel("Input")
        self.addWidget(self.text, 0, 0, 1, 2)
        self.addWidget(self.load, 1, 0, 1, 1)
        self.addWidget(self.reset, 1, 1, 1, 1)
        # self.addWidget(self.singleStep, 2, 0, 1, 1)
        # self.addWidget(self.fullExec, 2, 1, 1, 1)
        self.load.clicked.connect(self.load_input)
        self.reset.clicked.connect(self.reset_registers)

    @QtCore.pyqtSlot()
    def load_input(self):
        textInput = str(self.text.toPlainText())
        self.instructions = textInput.splitlines()
        self.opcode = Opcode(self.instructions)
        print(self.instructions)

        try:
            self.instruction_opcode = list(map(lambda x: self.opcode.get_opcode(x),self.instructions))
            self.pipeline = Pipeline(self.instructions,self.instruction_opcode)
            self.pipeline.get_pipeline()

            print(len(self.pipeline.values))
        except ValueError as ve:
            print(ve)
            return
        # except Exception as e:
        #     print(e)
        #     print('first')
        #     return
        print(self.frame)

    @QtCore.pyqtSlot()
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
        self.pipelineOutput = QtWidgets.QPlainTextEdit()
        self.memoryScroll = QtWidgets.QScrollArea()
        self.memoryTable = QtWidgets.QTableWidget()
        self.gpRegisterScroll = QtWidgets.QScrollArea()
        self.gpRegisterTable = QtWidgets.QTableWidget()
        self.cycleCtr = 0
        self.pipeline = Pipeline([''],[''])

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
        self.instructionTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.instructionTable.horizontalHeader().setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
        self.instructionScroll.setWidget(self.instructionTable)
        self.instructionScroll.setWidgetResizable(True)
        self.addWidget(self.opcode_label, 0, 0, 1, 1)
        self.addWidget(self.instructionScroll, 1, 0, 1, 1)

        # self.pipelineTable.setColumnCount(1)
        # self.pipelineTable.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Cycles"))
        # self.pipelineTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # self.pipelineScroll.setWidget(self.pipelineTable)
        # self.pipelineScroll.setWidgetResizable(True)
        # self.addWidget(self.pipelineLabel, 2, 0, 1, 1)
        # self.addWidget(self.pipelineScroll, 3, 0, 1, 1)

        self.addWidget(self.pipelineLabel, 2,0,1,1)
        self.addWidget(self.pipelineOutput, 3,0,1,1)

        self.gpRegisterTable.setColumnCount(2)
        self.gpRegisterTable.setRowCount(32)
        self.gpRegisterTable.setHorizontalHeaderItem(0,QtWidgets.QTableWidgetItem("GP Registers"))
        self.gpRegisterTable.setHorizontalHeaderItem(1,QtWidgets.QTableWidgetItem("Value"))
        self.gpRegisterTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.gpRegisterTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.gpRegisterScroll.setWidget(self.gpRegisterTable)
        self.gpRegisterScroll.setWidgetResizable(True)
        self.addWidget(self.gp_registers_label, 0, 1, 1, 1)
        self.addWidget(self.gpRegisterScroll, 1, 1, 1, 1)

        for x in range(0,32):
            print(x)
            self.gpRegisterTable.setItem(x, 0, QtWidgets.QTableWidgetItem("R"+str(x)))
            self.gpRegisterTable.setItem(x, 1, QtWidgets.QTableWidgetItem("0000000000000000"))

        self.memoryTable.setRowCount(4096)
        self.memoryTable.setColumnCount(2)
        self.memoryTable.setHorizontalHeaderItem(0,QtWidgets.QTableWidgetItem("Memory"))
        self.memoryTable.setHorizontalHeaderItem(1,QtWidgets.QTableWidgetItem("Value"))
        for x in range(0,4096):
            print(x)
            self.memoryTable.setItem(x, 0, QtWidgets.QTableWidgetItem(str(hex(x))))
            self.memoryTable.setItem(x, 1, QtWidgets.QTableWidgetItem("0000000000000000"))
        self.memoryTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.memoryTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.memoryScroll.setWidget(self.memoryTable)
        self.memoryScroll.setWidgetResizable(True)
        self.addWidget(self.mem_label, 2, 1, 1, 1)
        self.addWidget(self.memoryScroll, 3, 1, 1, 1)

        self.gotoMemory = QtWidgets.QLineEdit()
        self.gotoMemory.setPlaceholderText("GOTO Memory")
        self.addWidget(self.gotoMemory, 4,1,1,1)

        self.gotoButton = QtWidgets.QPushButton("GOTO Memory")
        self.gotoButton.clicked.connect(self.gotoAction)
        self.addWidget(self.gotoButton, 5,1,1,1)

    def gotoAction(self):
        needle = self.gotoMemory.text()
        out = self.memoryTable.findItems(needle, QtCore.Qt.MatchExactly)
        for item in out:
           self.memoryTable.setCurrentCell(item.row(), item.column())
    def get_pipeline(self, pipeline):
        self.pipeline = pipeline

        self.gotoButton = QtWidgets.QPushButton("GOTO Memory")
        self.addWidget(self.gotoButton, 5,1,1,1)

    def load_pipeline_from_input(self, pipeline):
        self.pipeline = pipeline
        print(self.pipeline)
        self.updateOpcode()
        self.updatePipeline()

    def i_sign_extend(self, value):
        mask = 0b1111111111111111
        if value[0] != '-':
            value = bin(int(value, 16))[2:].zfill(16)
        else:
            value = value[3:]
            value = int(bin(int(value, 16)), 2) ^ mask
            value = value + 0b1
            value = bin(value)[2:]
        sign = value[0]
        temp = [sign for x in range(64 - len(value))]
        temp = ''.join(temp)
        return temp + value

    def updateRegisterValues(self):
        for y in range(0, 32):
            self.gpRegisterTable.setItem(y, 0, QtWidgets.QTableWidgetItem("R" + str(y)))
            self.gpRegisterTable.setItem(y, 1, QtWidgets.QTableWidgetItem(str(hex(int(self.i_sign_extend(hex(self.pipeline.registers[self.cycleCtr].R[y])),2))[2:].zfill(16))))

    def updateMemory(self):
        for y in range(0,self.cycleCtr+1):
            for x in range(4096):
                self.memoryTable.setItem(x, 0, QtWidgets.QTableWidgetItem(str(hex(x))))
                self.memoryTable.setItem(x, 1, QtWidgets.QTableWidgetItem(str(self.pipeline.memory[y].memory[0][hex(x)])))

    def updateOpcode(self):
        self.clearOpcode()
        print(len(self.pipeline.instructions))
        if(len(self.pipeline.instructions) >= 1):
            self.instructionTable.setRowCount(len(self.pipeline.instructions))
            for ctr in range(0, len(self.pipeline.instructions)):
                self.currOpcode = bin(int(self.pipeline.opcode[ctr],16))[2:].zfill(32)
                indices = [0, 6, 11, 16, 21 ,26]
                self.parts = [self.currOpcode[i:j] for i, j in zip(indices, indices[1:] + [None])]
                print(self.parts)
                self.instructionTable.setItem(ctr, 0, QtWidgets.QTableWidgetItem(self.pipeline.instructions[ctr]))
                self.instructionTable.setItem(ctr, 1, QtWidgets.QTableWidgetItem(self.parts[0]))
                self.instructionTable.setItem(ctr, 2, QtWidgets.QTableWidgetItem(self.parts[1]))
                self.instructionTable.setItem(ctr, 3, QtWidgets.QTableWidgetItem(self.parts[2]))
                self.instructionTable.setItem(ctr, 4, QtWidgets.QTableWidgetItem(self.parts[3]))
                self.instructionTable.setItem(ctr, 5, QtWidgets.QTableWidgetItem(self.parts[4]))
                self.instructionTable.setItem(ctr, 6, QtWidgets.QTableWidgetItem(self.parts[5]))
                self.instructionTable.setItem(ctr, 7, QtWidgets.QTableWidgetItem(self.currOpcode))

    def updatePipeline(self):
        self.clearPipeline()
        print(len(self.pipeline.values))
        self.pipelineTable.setRowCount(len(self.pipeline.cycles)*5+len(self.pipeline.cycles))
        print()
        for x in range(0,self.cycleCtr+1):
            print(str(x))
            self.pipelineOutput.insertPlainText('Cycle '+str(x+1) + '\n')
            self.pipelineOutput.insertPlainText('IF = ' + str(self.pipeline.values[x][4]) + '\n')
            self.pipelineOutput.insertPlainText('ID = ' + str(self.pipeline.values[x][3]) + '\n')
            self.pipelineOutput.insertPlainText('EX = ' + str(self.pipeline.values[x][2]) + '\n')
            self.pipelineOutput.insertPlainText('MEM = ' + str(self.pipeline.values[x][1]) + '\n')
            self.pipelineOutput.insertPlainText('WB = ' + str(self.pipeline.values[x][0]) + '\n')
            # self.pipelineTable.setItem(x+1, 0, QtWidgets.QTableWidget("Cycle " + str(x)))
            # self.pipelineTable.setItem(x+3, 0, QtWidgets.QTableWidgetItem(str(self.pipeline.values[x].if_id.IR)))
            # self.pipelineTable.setItem(x+^, 0, QtWidgets.QTableWidgetItem(self.pipeline.values[x].id_ex.IR))
            # self.pipelineTable.setItem(x*4, 0, QtWidgets.QTableWidgetItem(self.pipeline.values[x].ex_mem.IR))
            # self.pipelineTable.setItem(x*5, 0, QtWidgets.QTableWidgetItem(self.pipeline.values[x].mem_wb.IR))
            # self.pipelineTable.setItem(x*6, 0, QtWidgets.QTableWidgetItem(self.pipeline.values[x].wb.IR))

        #self.pipelineTable.setRowCount(len(self.pipeline.cycles))
    def clearPipeline(self):
        self.pipelineOutput.clear()
        #self.pipelineTable.clearContents()

    def clearRegistervalues(self):
        pass
    def clearOpcode(self):
        self.instructionTable.clearContents()

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
        print(self.tabs.widget(0))

    def pass_pipeline(self):
        self.output_tabs.layout.load_pipeline_from_input(self.input_tabs.layout.pipeline)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
