from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt
import sys


# This class window extends from the QWidget class, which is the base class of all user interface objects
class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("player.png"))
        self.setWindowTitle("Python Media Player")
        self.setGeometry(350, 100, 700, 500)

        # Set color for window
        p = self.palette()
        # TODO: Find a color that works for the project
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.create_player()

    # Creating multimedia functionality
    def create_player(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.openButton = QPushButton('Open Video')

        """
        The QHbox Layout lines up the widgets Horizontally
        Variable: hbox for Horizontal Box
        """

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addWidget(self.openButton)

        """
        The QVbox Layout lines up the widgets Vertically
        Variable: vbox for Horizontal Box
        """

        vbox = QVBoxLayout()

        vbox.addLayout(hbox)

        # Need to set main window layout, which should be the vertical box layout
        self.setLayout(vbox)





app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
