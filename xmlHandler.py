import xml.sax
"""
Class design inspiration from https://www.tutorialspoint.com/parsing-xml-with-sax-apis-in-python
"""
class FileHandler(xml.sax.ContentHandler):

    def __init__(self):
        self.currentData = ""
        self.fileID = ""
        self.instrumentSetting = ""
        self.playStyle = ""
        self.midi = ""
        self.string = ""
        self.fret = ""
        self.fxGroup = ""
        self.fxType = ""
        self.fxSetting = ""
        self.fileTag = ""
        self.dict = {"fileID":[], "instrumentSetting":[], "playStyle":[], 
                     "midi":[], "string":[], "fret":[], "fxGroup":[], 
                     "fxType":[], "fxSetting":[], "fileTag":[]}
    
    def startElement(self, tag, attributes):
        self.currentData = tag
    
    def endElement(self, tag):
        if self.currentData == "fileID":
            self.dict["fileID"].append(self.fileID)
        elif self.currentData == "instrumentsetting":
            self.dict["instrumentSetting"].append(self.instrumentSetting)
        elif self.currentData == "playstyle":
            self.dict["playStyle"].append(self.playStyle)
        elif self.currentData == "midinr":
            self.dict["midi"].append(self.midi)
        elif self.currentData == "string":
            self.dict["string"].append(self.string)
        elif self.currentData == "fret":
            self.dict["fret"].append(self.fret)
        elif self.currentData == "fxgroup":
            self.dict["fxGroup"].append(self.fxGroup)
        elif self.currentData == "fxsetting":
            self.dict["fxSetting"].append(self.fxSetting)
        elif self.currentData == "fxtype":
            self.dict["fxType"].append(self.fxType)
        elif self.currentData == "filenr":
            self.dict["fileTag"].append(self.fileTag)
        self.currentData = ""
            
    def characters(self, tag):
        if self.currentData == "fileID":
            self.fileID = tag
        elif self.currentData == "instrumentsetting":
            self.instrumentSetting = tag
        elif self.currentData == "playstyle":
            self.playStyle = tag    
        elif self.currentData == "midinr":
            self.midi = tag    
        elif self.currentData == "string":
            self.string = tag    
        elif self.currentData == "fret":
            self.fret = tag  
        elif self.currentData == "fxgroup":
            self.fxGroup = tag  
        elif self.currentData == "fxsetting":
            self.fxSetting = tag 
        elif self.currentData == "fxtype":
            self.fxType = tag 
        elif self.currentData == "filenr":
            self.fileTag = tag 