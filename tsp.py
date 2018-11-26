import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from branchandbound.BrandAndBoundTSP import BranchAndBound
from Generator import Generator

class TSP(QDialog):
    def __init__(self):
        super(TSP, self).__init__()
        loadUi("UI/TSP.ui", self)
        # List of available algorithms
        algos = ["Brute Force", "Branch and Bound", "Greedy", "Minimum Spanning Tree"]
        self.cboAlgo.clear()
        self.cboAlgo.addItems(algos)
        self.btnRun.clicked.connect(self.on_run_clicked)
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

    @pyqtSlot()
    def on_run_clicked(self):
        #first of all see what is selected from the data options
        if self.optGenerate.isChecked():
            #TODO validate user entries
            numVert = int(self.txtVertices.text())
            connect = int(self.txtConnect.text())
            minWgt = int(self.txtMin.text())
            maxWgt = int(self.txtMax.text())
            symmetric = self.chkSym.isChecked()
            # Create a new generator.
            generator = Generator()
            # Generate a new matrix with given parameters.
            matrix = generator.generate(numVert, connect, minWgt, maxWgt, symmetric)

        if self.cboAlgo.currentText() == "Branch and Bound":
            algo = BranchAndBound()
            upper_bound, best_path = algo.run_branch_and_bound(matrix)
            self.lblDistance.setText("Best Distance: " + str(upper_bound))
            self.lblPath.setText("Best Path: " + str(best_path))

app=QApplication(sys.argv)
window = TSP()
window.show()
sys.exit(app.exec_())
