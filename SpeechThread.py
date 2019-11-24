from PyQt5.QtCore import QThread, pyqtSignal
from google_speech import googleSpeechHandler


class SpeechThread(QThread):

    new_message = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.gsh = None

    def __del__(self):
        self.wait()

    def gshCallback(self, message):
        self.new_message.emit(message)

    def run(self):
        self.gsh = googleSpeechHandler()
        self.gsh.startDetectionService(self.gshCallback)
