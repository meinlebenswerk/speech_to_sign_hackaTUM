from PyQt5.QtCore import pyqtSignal, QObject
import os


class text2video(QObject):

    MAXLEN = 4

    newDataAvailable = pyqtSignal()

    def __init__(self, widget):
        super(text2video, self).__init__()
        self.widget = widget

        print('Loading sign-db(s)')
        self.db = []
        self.words = []
        self.nextVideos = []
        self._makeDB()

    def _makeDB(self):
        videofiles = [f for f in os.listdir('data/video') if os.path.isfile(os.path.join('data/video', f))]
        for file in videofiles:
            word = file.split('.')[0].replace('_', ' ')
            self.db.append(word)

    def sentenceParsed(self, sentence):
        _words = sentence.lower().split(' ')
        for word in _words:
            self.words.append(word)

        while len(self.words) > 0:
            self._lookupNext()

    def _lookupNext(self):
        lastmatch = None
        matchlen = 0
        for i in range(text2video.MAXLEN):
            lookup = ' '.join(self.words[0:i+1])
            # print('lookup:', lookup)
            if lookup in self.db:
                lastmatch = lookup
                matchlen = i+1

        print('matchlen:', matchlen)

        if lastmatch is None:
            # remove last element from self.words
            chars = list(self.words[0])
            self.words = self.words[1:]
            for i in range(len(chars)):
                self.nextVideos.append(chars[i])
        else:
            self.words = self.words[matchlen:]
            self.nextVideos.append(lastmatch.replace(' ', '_'))

        self.newDataAvailable.emit()



    def getNextVideo(self):
        if len(self.nextVideos) == 0:
            return None
        else:
            return self.nextVideos.pop(0)


if __name__ == '__main__':
    t2v = text2video()
    #url = t2v.getVideoURL('help')
    #t2v._checkDB()

