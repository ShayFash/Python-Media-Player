from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, \
    QStyle, QSlider, QFileDialog
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
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


    def create_player(self):
        """
        Creating Multimedia functionality
        :return:
        """
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videowidget = QVideoWidget()

        # Add Button for Open Video
        self.openButton = QPushButton('Open Video')
        self.openButton.clicked.connect(self.open_file)

        # Add Button for Play Video
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play_video)

        # Add Video Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)

        """
        The QHbox Layout lines up the widgets Horizontally
        Variable: hbox for Horizontal Box
        """

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addWidget(self.openButton)
        hbox.addWidget(self.playButton)
        hbox.addWidget(self.slider)

        """
        The QVbox Layout lines up the widgets Vertically
        Variable: vbox for Horizontal Box
        """

        vbox = QVBoxLayout()
        vbox.addWidget(videowidget)

        vbox.addLayout(hbox)
        self.mediaPlayer.setVideoOutput(videowidget)

        # Need to set main window layout, which should be the vertical box layout
        self.setLayout(vbox)

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def open_file(self):
        """
        Open file dialogue box, so we can open files from computer
        :return:
        """
        filename, _ = QFileDialog.getOpenFileNames(self, "Open Video")
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename[0])))
            self.playButton.setEnabled(True)

    def play_video(self):
        """
        Video playing functionality
        :return:
        """
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        """
        Determines state of the video, is it playing or not and changes icons from play to pause
        :param state:
        :return:
        """
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        """
        Determines position of video for the slider
        :param position:
        :return:
        """
        self.slider.setValue(position)

    def duration_changed(self, duration):
        """
        Set duration changed for slider
        :param duration:
        :return:
        """
        self.slider.setRange(0, duration)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
