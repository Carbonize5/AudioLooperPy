from PySide6.QtMultimedia import QMediaPlayer

class Tag():

    def __init__(self):
        self.position : int = None
    
    def __init__(self, pos : int):
        self.position : int = pos
    
    def getPosition(self):
        return self.position
    
    def setPosition(self, new_pos):
        self.position = new_pos
    
    def toUI(self):
        return "At " + str(self.position)

    def toPyJSON(self) -> dict:
        d = dict()
        d["Type"] = 0
        d["Args"] = [self.position]
        return d
    
    def useTag(self, mediaPlayer : QMediaPlayer):
        print("Tag Used, MediaPlayer: " + mediaPlayer.__str__())

class GoToTag(Tag):
    
    def __init__(self, pos : int, dest : int):
        super().__init__(pos)
        self.destination : int = dest
    
    def getDestination(self):
        return self.destination
    
    def setDestination(self, new_dest):
        self.destination = new_dest
    
    def toUI(self):
        return "At " + str(self.position) + " go to " + str(self.destination)
    
    def toPyJSON(self) -> dict:
        d = super().toPyJSON()
        d["Type"] = 1
        d["Args"].append(self.destination)
        return d

    def __str__(self):
        return "GoToTag("+self.position.__str__()+","+self.destination.__str__()+")"
    
    def useTag(self, mediaPlayer : QMediaPlayer):
        # super().useTag(mediaPlayer)
        mediaPlayer.setPosition(self.destination)