class Tag():

    def __init__(self):
        self.position : int = None
    
    def __init__(self, pos : int):
        self.position : int = pos
    
    def getPosition(self):
        return self.position
    
    def setPosition(self, new_pos):
        self.position = new_pos
    
    def __str__(self):
        pass

class GoToTag(Tag):

    def __init__(self):
        super().__init__()
        self.destination : int = None
    
    def __init__(self, pos : int, dest : int):
        super().__init__(pos)
        self.destination : int = dest
    
    def getDestination(self):
        return self.destination
    
    def setDestination(self, new_dest):
        self.destination = new_dest
    
    def __str__(self):
        return "At " + str(self.position) + " go to " + str(self.destination)