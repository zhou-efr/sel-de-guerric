"""object.py
    this file contain all objects needed
    for instance:
        items

author : la tribut des zhou
"""
import pygame
import loaders as l

pygame.init()

class item:
    """item, the main class, all others object are inherent to this one
        Work In Progress (wip)
        j'ai fait ce dont j'avais besoin je vous laisserai probablement le reste vue que c'est du backend
        C'est pas par ce que je l'ai cree que vous avez a la garder
    """
    def __init__(self, keyChar, environment):
        self.keyChar = keyChar
        self.pictureAdress = "./files/environment" + str( environment) + "/" + keyChar + ".png"
        self.picture = pygame.image.load(self.pictureAdress)
        self.position = {"x1" : 0, "y1" : 0, "x2" : 0, "y2" : 0}
    #---end init---

    #---beginning accessors
    def getKeyChar(self):
        return self.keyChar
    
    def getPictureAdress(self):
        return self.pictureAdress
    
    def getPicture(self):
        return self.picture

    def getPosition(self):
        return self.position
    #---end accessors---

class entities (item):

    def __init__(self, keyChar, environment):
        super().__init__(keyChar, environment)
        self.folder = "./files/environment" + str(environment)+"/" + keyChar + "/"
        self.data = {}
        self.sprite = []
        self.internalClock = -1
        self.changed = False
        self.speed = 0
        self.acceleration = 0
        contents = []
        try:
            self.data = l.fileLoader(self.folder, str(keyChar) + ".dat")
        except (FileNotFoundError, IndexError) as identifier:
            print(identifier)
            self.data = {"sprite" : 1, "x" : 2.0, "y" : 2.0}# faut update le default case mais j'ai la flemme
        #---end try---
        self.data["newState"] = None
        self.updateSprite()
    #---end init---

    def internalClockUpdate(self):
        if (self.internalClock >= (self.data[self.data["state"]]["index"] - 1)):
            self.internalClock = -1
        #---end if---
        self.internalClock += 1
    #--end iternalClockUpdate---

    def getPicture(self):
        if self.changed and self.data[self.data["state"]]["initialState"] == self.internalClock:
            self.data["state"] = self.data["newState"]
            self.updateSprite()
        #---end if---
        self.internalClockUpdate()
        return self.sprite[self.internalClock]
        
    #---end getPicture---

    def getPosition(self):
        return self.data["x"], self.data["y"]
    #---end getPosition---

    def updateSprite(self):
        self.sprite = []
        for i in range(self.data[self.data["state"]]["index"]):
            self.sprite.append(pygame.image.load(self.folder + "sprite/" + self.data["state"] + "/sprt" + str(i) + ".png").convert_alpha())
        #---end for---
    #---end updateSprite---

    def changeState(self, dead = 0):
        if dead:
            self.data["state"] = "dead"
        #---end if---
        self.changed = True
    #---end changeState---

    #---beginning accessors---
    def getSpeed(self):
        return self.speed
    
    def getAcceleration(self):
        return self.acceleration
    #---end accessors---
#---end entities---

class player (entities):

    def __init__(self):
        super().__init__('p', 0)
    #---end init---

    def changeState(self, dead = 0):
        super().changeState(dead)
        if not(dead):
            if self.data["state"] == "bouncing" :
                self.data["newState"] = "static"
            elif self.data["state"] == "static":
                self.data["newState"] = "bouncing"
            #---end if---
        #---end if---
    #---end changeState---
#---end player---  