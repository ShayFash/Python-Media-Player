import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.resize(860, 600)
        self.setWindowTitle('Python Video Player')
        self.setWindowIcon(QIcon("player.png"))
        self.ui_init()

    # Media Player UI
    def ui_init(self):
        # Menubar objects
        menu = self.menuBar()
        file = menu.addMenu("File")
        file.addAction("Open File")
        file.triggered[QAction].connect(self.open_file)




