from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl

class TranslatorWidget(QWidget):

    def __init__(self, window):
        super(TranslatorWidget, self).__init__()
        self.window = window
        self.recording = False

        self.setup_ui()
        self.window.setLayout(self.layout)

        self.buttonRecord.clicked.connect(self.pbRecordHandler)

    def setup_ui(self):
        # Load the font:
        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont("Roboto-Medium.ttf")

        self.layout = QVBoxLayout()

        self.menuLabel = QLabel("Listening, please speak now...")
        self.menuLabel.setFont(QFont("Roboto", 14, QFont.Medium))
        self.menuLabel.setWordWrap(True)
        self.layout.addWidget(self.menuLabel)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.layout.addWidget(self.videoWidget)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.error.connect(self.displayErrorMessage)

        """
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        """

        self.buttonRecord = QPushButton('rec')
        self.layout.addWidget(self.buttonRecord)

    def displayErrorMessage(self):
        print(self.mediaPlayer.errorString())

    def pbRecordHandler(self):
        self.recording = not self.recording
        # state-logic
        print(self.recording)
        self._playVideoFile('/home/jan/Documents/hackaTUM/scrapieboi/a.mp4')

    def _playVideoFile(self, path):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.mediaPlayer.play()
        print(self.mediaPlayer.isAvailable())




app = QApplication([])
window = QWidget()
window.setFixedWidth(480)
window.setFixedHeight(854)

tw = TranslatorWidget(window)

window.show()
app.exec_()