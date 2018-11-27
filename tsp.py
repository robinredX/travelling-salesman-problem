import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt5.uic import loadUi
from branchandbound.BrandAndBoundTSP import BranchAndBound
from Generator import Generator
from Parser import Parser

class TSP(QDialog):
    def __init__(self):
        super(TSP, self).__init__()
        loadUi("UI/TSP.ui", self)
        # List of available algorithms
        algos = ["Brute Force", "Branch and Bound", "Add and Remove Edges", "Random", "Greedy", "Minimum Spanning Tree", "Ant Colony", "Dynamic"]
        self.cboAlgo.clear()
        self.cboAlgo.addItems(algos)
        formats = ["Generator", "TSP Library"]
        self.cboFormat.addItems(formats)
        self.frmUpload.move(10, 140)
        self.frmUpload.setHidden(True)

        self.btnRun.clicked.connect(self.on_run_clicked)
        self.btnBrowse_Open.clicked.connect(self.on_browse_open_clicked)
        self.btnBrowse_Save.clicked.connect(self.on_browse_save_clicked)
        self.btnClose.clicked.connect(self.close)
        self.optGenerate.toggled.connect(self.optGenerate_clicked)
        self.optExisting.toggled.connect(self.optExisting_clicked)

    def optGenerate_clicked(self):
        self.frmGenerate.setEnabled(self.optGenerate.isChecked())
        self.frmGenerate.setHidden(False)
        self.frmUpload.setHidden(True)

    def optExisting_clicked(self):
        self.frmGenerate.setEnabled(self.optGenerate.isChecked())
        self.frmGenerate.setHidden(True)
        self.frmUpload.setHidden(False)

    def on_browse_open_clicked(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '\data')
        self.txtFileName.setText(fname[0])

    def on_browse_save_clicked(self):
        fname = QFileDialog.getSaveFileName(self, 'Open file', '\data')
        self.txtSaveAs.setText(fname[0])

    @pyqtSlot()
    def on_run_clicked(self):
        # Create a new generator.
        generator = Generator()
        #first of all see what is selected from the data options
        if self.optGenerate.isChecked():
            #TODO validate user entries
            numVert = int(self.txtVertices.text())
            connect = int(self.txtConnect.text())
            minWgt = int(self.txtMin.text())
            maxWgt = int(self.txtMax.text())
            symmetric = self.chkSym.isChecked()
            # Generate a new matrix with given parameters.
            matrix = generator.generate(numVert, connect, minWgt, maxWgt, symmetric)
            #if the Save_As text box is not empty, save for later.
            generator.save_to_file(matrix, self.txtSaveAs.text())
        else:
            #Open and process the selected file
            if self.cboFormat.currentText() == "Generator":
                matrix = generator.read_from_file(self.txtFileName.text())

        if self.cboAlgo.currentText() == "Branch and Bound":
            algo = BranchAndBound()
            time = 0 # add timer here
            upper_bound, best_path = algo.run_branch_and_bound(matrix)
            self.lblDistance.setText("Best Distance: " + str(upper_bound))
            self.lblPath.setText("Best Path: " + str(best_path))
            self.lblExec.setText("Execution Time: " + str(time))

app=QApplication(sys.argv)
window = TSP()
window.show()
sys.exit(app.exec_())
