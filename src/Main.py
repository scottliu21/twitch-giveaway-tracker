from GUI.MainWindow import MainWindow
import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec_())