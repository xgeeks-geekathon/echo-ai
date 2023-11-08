import os

mediaPath = 'media/'
jsonExtension = ".json"
srtExtension = ".srt"

class ParsedFile:
    name = ""
    path = ""
    extension = ""

    def __init__(self, tempPath):
        self.path = tempPath
        self.name, self.extension =os.path.splitext(os.path.basename(tempPath))

    def getTranscribePath(self):
        return mediaPath + self.name + jsonExtension
    
    def getTranslatePath(self):
        return mediaPath + self.name + '_translation' + jsonExtension
    
    def getTranscribeSrtPath(self):
        return mediaPath + self.name + srtExtension
    
    def getTranslateSrtPath(self):
        return mediaPath + self.name + '_translation' + srtExtension
