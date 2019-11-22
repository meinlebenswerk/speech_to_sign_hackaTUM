import urllib.request
import requests
import json

def HTTP_GET(url):
    fp = urllib.request.urlopen(url)
    if fp.getcode == 404:
        print('Oh no.')
    mybytes = fp.read()

    data = mybytes.decode("utf8")
    fp.close()

    return data

def HTTP_STATUS_CHECK(url):
    req = requests.head(url)
    return req.status_code

def LOAD_FILE(path):
    with open(path, 'r') as content_file:
        content = content_file.read()
        return content


class text2video:

    def __init__(self):
        print('Loading sign-db(s)')
        self._loadDB()

    def _parseHandSpeakEntry(self, entry):
        id = entry["signID"]
        name = entry["signName"].lower()
        url = "https://www.handspeak.com/word/search/index.php?id={}".format(id)
        site = HTTP_GET(url)
        print(site)
        import os
        os._exit(1)
        return name

    def _loadDB(self):
        print('Loading db from handspeak.com')
        raw = LOAD_FILE("/home/jan/Documents/hackaTUM/db.txt")
        #self.db = HTTP_GET("https://www.handspeak.com/word/search/app/getlist.php")
        self.json_db = json.loads(raw)
        self.db = list(map(self._parseHandSpeakEntry, self.json_db))
        print('loaded {} records into db'.format(len(self.json_db)))
        # print(self.db)

    def _checkDB(self):
        for word in self.db:
            print(word)

    """ return either a valid video-url or None :) """
    def getVideoURL(self, sign):
        url = "https://www.handspeak.com/word/{}/{}.mp4".format(sign.lower()[0], sign)
        status = HTTP_STATUS_CHECK(url)
        if status == 400:
            print('could not load sign {}'.format(sign))
            return None
        return url

def getVideo(sign):
    fp = urllib.request.urlopen("https://www.handspeak.com/word/search/app/getlist.php")
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    print(mystr)

if __name__ == '__main__':
    t2v = text2video()
    #url = t2v.getVideoURL('help')
    #t2v._checkDB()
