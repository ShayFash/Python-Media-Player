from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt
import sys


# This class window extends from the QWidget class, which is the base class of all user interface objects
class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("player.png"))
        self.setWindowTitle("Python Media Player")
        self.setGeometry(350,100,700, 500)

        # Set color for window
        p = self.palette()
        # TODO: Find a color that works for the project
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
