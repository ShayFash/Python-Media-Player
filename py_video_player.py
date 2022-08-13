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
        # ---- Creating Media Objects ---- #
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

        # ----- Creating Playlist QListView widget ------ #
        self.playlistView = QListView()
        self.playlistView.setAlternatingRowColors(True)
        self.playlistView.setUniformItemSizes(True)

        self.model = PlaylistModel(self.playlist)
        self.playlistView.setModel(self.model)
        self.playlist.currentIndexChanged.connect(self.playlist_position_changed)

        selection_model = self.playlistView.selectionModel()
        selection_model.selectionChanged.connect(self.playlist_selection_changed)
        self.playlistView.doubleClicked.connect(self.ply)

        self.p_play = QPushButton("  Play Now ")
        self.p_play.setStyleSheet('background-color: rgb(32, 32, 32)')
        self.p_play.setEnabled(False)
        self.p_play.clicked.connect(self.ply)

        self.rm = QPushButton(" Remove ")
        self.rm.setToolTip('Remove Item from Playlist')
        self.rm.setStyleSheet('background-color: rgb(32, 32, 32)')
        self.rm.setEnabled(False)
        self.rm.clicked.connect(self.remove)

        self.playback_Label = QLabel("")
        self.playback_Label.setToolTip('Playback Mode')
        self.playback_Label.setFixedWidth(200)
        self.playback_Label.setStyleSheet(
            "color: silver;""border-style: solid;""border-width: 1px;""border-color: rgba(250, 128, 114, 95);""border-radius: 10px")
        self.playback_Label.setAlignment(Qt.AlignCenter)
        self.playback_Label.setText("Current Playlist is in Loop Off")

        # ----- Creating time progress widgets ------ #
        self.currentTimeLabel = QLabel()
        self.currentTimeLabel.setMinimumSize(80, 0)
        self.currentTimeLabel.setAlignment(Qt.AlignCenter)
        self.currentTimeLabel.setText(hhmmss(0))

        self.time_slider = QSlider(Qt.Horizontal)
        self.time_slider.setRange(0, 0)
        self.time_slider.sliderMoved.connect(self.set_position)

        self.totalTimeLabel = QLabel()
        self.totalTimeLabel.setMinimumSize(80, 0)
        self.totalTimeLabel.setAlignment(Qt.AlignCenter)
        self.totalTimeLabel.setText(hhmmss(0))

        # ------ Creating Control widgets ---------- #
        self.plist = QPushButton(" Playlist")
        self.plist.setIcon(QIcon(":/icons/plist.png"))
        self.plist.setToolTip("Show Playlist")
        self.plist.clicked.connect(self.plistview)
        self.plist.installEventFilter(self)

        self.previous = QPushButton(" Prev")
        self.previous.setIcon(QIcon(":/icons/previous.png"))
        self.previous.pressed.connect(self.playlist.previous)
        self.previous.setEnabled(False)
        self.previous.installEventFilter(self)

        self.next = QPushButton(" Next")
        self.next.setIcon(QIcon(":/icons/next.png"))
        self.next.pressed.connect(self.playlist.next)
        self.next.setEnabled(False)
        self.next.installEventFilter(self)

        self.skip_back = QPushButton()
        self.skip_back.setIcon(QIcon(":/icons/skip_back.png"))
        self.skip_back.setToolTip('Skip 5 sec backward')
        self.skip_back.setEnabled(False)
        self.skip_back.clicked.connect(self.backward)
        self.skip_back.installEventFilter(self)

        self.play = QPushButton()
        self.play.setIcon(QIcon(":/icons/play.png"))
        self.play.setToolTip("Play/Pause")
        self.play.setEnabled(False)
        self.play.pressed.connect(self.play_video)

        self.stop = QPushButton()
        self.stop.setIcon(QIcon(":/icons/stop.png"))
        self.stop.setToolTip("Stop")
        self.stop.setEnabled(False)
        self.stop.pressed.connect(self.mediaPlayer.stop)
        self.stop.installEventFilter(self)

        self.skip_forward = QPushButton()
        self.skip_forward.setIcon(QIcon(":/icons/skip_frwd.png"))
        self.skip_forward.setToolTip('Skip 5 sec forward')
        self.skip_forward.setEnabled(False)
        self.skip_forward.clicked.connect(self.forward)
        self.skip_forward.installEventFilter(self)

        self.playback = QPushButton("")
        self.playback.setIcon(QIcon(":/icons/loop_off.png"))
        self.playback.setToolTip(" Playback Mode ")
        self.playback.clicked.connect(self.playback_mode)
        self.playback.setEnabled(False)
        self.playback.installEventFilter(self)

        self.mute = QPushButton()
        self.mute.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.mute.clicked.connect(self.mute_fn)
        self.mute.installEventFilter(self)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setProperty('value', 50)
        self.volume_slider.valueChanged.connect(self.mediaPlayer.setVolume)

        self.aspr = QPushButton()
        self.aspr.setIcon(QIcon(":/icons/aspr.png"))
        self.aspr.setStyleSheet('border-radius: 5px ;''background-color:#626262')
        self.aspr.setToolTip("Aspect Ratio")
        self.aspr.setCheckable(True)
        self.aspr.setEnabled(False)
        self.aspr.toggled.connect(self.aspRatio)
        self.aspr.installEventFilter(self)


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


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Doing a dark palette color scheme
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(16, 16, 16))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(65, 65, 65))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid silver; }")

    # Create a window object
    mp = Window()
    mp.show()
    sys.exit(app.exec_())


def hhmmss(ms):
    """
    function to convert from milliseconds to hh:mm:ss
    :param ms:
    :return: hh:mm:ss
    """
    s = round(ms / 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return ("%d:%02d:%02d" % (h, m, s)) if h else ("%d:%02d" % (m, s))
