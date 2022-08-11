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

        # Creating Media Objects
        self.mediaPlayer = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.mediaPlayer.setPlaylist(self.playlist)

        self.videoItem = QGraphicsVideoItem()
        self.videoItem.setAspectRatioMode(Qt.KeepAspectRatio)

        scene = QGraphicsScene(self)
        graphicsView = QGraphicsView(scene)
        graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scene.addItem(self.videoItem)

        self.mediaPlayer.setVideoOutput(self.videoItem)
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)




class PlaylistModel(QAbstractListModel):
    def __init__(self, playlist, *args, **kwargs):
        super(PlaylistModel, self).__init__(*args, **kwargs)
        self.playlist = playlist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            media = self.playlist.media(index.row())
            return media.canonicalUrl().fileName()

    def rowCount(self, index):
        return self.playlist.mediaCount()