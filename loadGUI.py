from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QSplashScreen, QMainWindow, QStackedWidget
from PyQt5.QtGui import QFontDatabase, QFont, QIcon, QPixmap, QShowEvent, QColor
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, pyqtSignal, Qt, QSize, QTimer

from google_speech import googleSpeechHandler
from text2video import text2video
from SpeechThread import SpeechThread

import os
import time

class MainWindow(QMainWindow):

    def __init__(self, parent=None, timer=None):
        super(MainWindow, self).__init__(parent)
        self.timer = timer
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        splashwidget = SplashScreen()
        self.central_widget.addWidget(splashwidget)

    def splash(self):
        translator = TranslatorWidget()
        self.central_widget.addWidget(translator)
        self.central_widget.setCurrentWidget(translator)
        
    def showEvent(self, a0: QShowEvent):
        super(MainWindow, self).showEvent(a0)
        if self.timer is not None:
            self.timer.start(800)



class TranslatorWidget(QWidget):

    LABEL_OFF = "To start, press the button"
    LABEL_ON = "Try saying something"

    def __init__(self):
        super(TranslatorWidget, self).__init__()
        self.recording = False

        self.setup_ui()
        self.setLayout(self.layout)
        # self.window.setLayout(self.layout)

        self.buttonRecord.clicked.connect(self.pbRecordHandler)

        self.t2v = text2video(self)
        self.t2v.newDataAvailable.connect(self._queryNextVideo)

        self.gsThread = SpeechThread()
        self.gsThread.new_message.connect(self.t2v.sentenceParsed)

    def setup_ui(self):
        # Load the font:
        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont("Roboto-Medium.ttf")

        self.layout = QVBoxLayout()

        self.menuLabel = QLabel(TranslatorWidget.LABEL_OFF)
        self.menuLabel.setFont(QFont("Roboto", 14, QFont.Medium))
        self.menuLabel.setWordWrap(True)
        self.menuLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.menuLabel)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.layout.addWidget(self.videoWidget)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.error.connect(self.displayErrorMessage)
        self.mediaPlayer.stateChanged.connect(self._checkMediaState)

        """
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        """

        self.buttonRecord = QPushButton('')
        self.buttonRecord.setIcon(QIcon('data/baseline_touch_app_white_48dp.png'))
        self.buttonRecord.setIconSize(QSize(64, 64))
        self.buttonRecord.setProperty("state", "inactive")
        # self.buttonRecord.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.buttonRecord, alignment=Qt.AlignHCenter)

        styleFile = os.path.join(os.path.split(__file__)[0], "style.qss")
        styleSheetStr = open(styleFile, "r").read()
        window.setStyleSheet(styleSheetStr)

    def displayErrorMessage(self):
        print(self.mediaPlayer.errorString())

    def pbRecordHandler(self):
        self.recording = not self.recording
        if self.recording:
            self.gsThread.start()
            self.menuLabel.setText(TranslatorWidget.LABEL_ON)
            self.buttonRecord.setProperty("state", "active")
            self.buttonRecord.setIcon(QIcon('data/baseline_pause_white_48dp.png'))
            self.buttonRecord.setIconSize(QSize(64, 64))
            self.buttonRecord.style().unpolish(self.buttonRecord)
            self.buttonRecord.style().polish(self.buttonRecord)
            self.buttonRecord.update()
        else:
            self.menuLabel.setText(TranslatorWidget.LABEL_OFF)
            self.buttonRecord.setProperty("state", "inactive")
            self.buttonRecord.setIcon(QIcon('data/baseline_touch_app_white_48dp.png'))
            self.buttonRecord.setIconSize(QSize(64, 64))
            self.buttonRecord.style().unpolish(self.buttonRecord)
            self.buttonRecord.style().polish(self.buttonRecord)
            self.buttonRecord.update()
            self.gsThread.terminate()

    def _playVideoFile(self, path):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.mediaPlayer.play()

    def _queryNextVideo(self):
        if self.mediaPlayer.state() == 1:
            return

        # print('QueryNextVideo!')
        nv = self.t2v.getNextVideo()
        if nv is not None:
            path = os.path.join(os.getcwd(), 'data', 'video', '{}.mp4'.format(nv))
            print(os.path.abspath(path))
            self._playVideoFile(path)

    def _checkMediaState(self, state):
        if state == 0:
            self._queryNextVideo()


class SplashScreen(QWidget):

    def __init__(self):
        super(SplashScreen, self).__init__()

        self.loadUI()
        self.setLayout(self.layout)
        self.show()

    def loadUI(self):
        self.layout = QVBoxLayout()

        self.imgLabel = QLabel(self)
        pixmap = QPixmap('data/logo.png')
        self.imgLabel.setPixmap(pixmap)
        self.imgLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.imgLabel)


width = int(480*1.3)
height = int(854*1.3)

app = QApplication([])
timer = QTimer()
timer.setSingleShot(True)
window = MainWindow(timer=timer)
window.setFixedWidth(width)
window.setFixedHeight(height)
timer.timeout.connect(window.splash)
window.show()

app.exec_()


