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
        self.state = "default"
        self.folder = "./files/environment" + str(environment) + "/items/" + keyChar + "/"
        self.pictureAdress = self.folder + self.state + ".png"
        self.picture = pygame.image.load(self.pictureAdress)
        self.updateObjectPictureSize()
        self.position = {"x1" : 0, "y1" : 0, "x2" : 0, "y2" : 0}
    #---end init---

    def updateObjectPictureSize(self, size = 120):
        self.picture = pygame.transform.scale(self.picture.convert_alpha(), (size, size))
    #---end updatePictureSize---

    def updateState(self, newstate):
        self.state = newstate
        self.pictureAdress = self.folder + self.state + ".png"
        self.picture = pygame.image.load(self.pictureAdress)
    #---end updateState---

    #---beginning accessors
    def getKeyChar(self):
        return self.keyChar

    def getFolder(self):
        return self.folder
    
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
        self.dataFolder = self.folder + "data/"
        self.data = {}
        self.sprite = []
        self.internalClock = -1
        self.clock = -1
        self.changed = False
        self.hit = False
        self.speed = {"x" : 0,"y" : 0}
        self.acceleration = {"x" : 0,"y" : 0}
        self.inptime = 0
        try:
            self.data = l.fileLoader(self.dataFolder, str(keyChar) + ".dat")
        except (FileNotFoundError, IndexError) as identifier:
            print(identifier)
            self.data = {"state" : "na", "na" : {"index" : 0}}
        #---end try---
        self.data["newState"] = None
        self.updateSprite()
    #---end init---

    def internalClockUpdate(self):
        if (self.internalClock >= (self.data[self.data["state"]]["index"] - 1)):
            self.internalClock = -1
        #---end if---

        if (self.clock >= (self.data[self.data["state"]]["duration"] - 1)):
            self.clock = -1
        #---end if---

        if (self.clock == -1):
            self.internalClock += 1
        #---end if---

        self.clock += 1
    #--end iternalClockUpdate---

    def getPicture(self):
        if self.changed and self.data[self.data["state"]]["initialState"] == self.internalClock:
            self.data["state"] = self.data["newState"]
            self.updateSprite()
        #---end if---
        self.internalClockUpdate()
        return self.sprite[self.internalClock]
    #---end getPicture---

    def updatePictureSize(self, size = 120):
        for i in range(len(self.sprite)):
            self.sprite[i] = pygame.transform.scale(self.sprite[i].convert_alpha(), (size, size))
        #---end for---
    #---end updatePictureSize---

    def getPosition(self):
        return self.position["x1"], self.position["y1"], self.position["x2"], self.position["y2"]
    #---end getPosition---

    def updateSprite(self):
        self.sprite = []
        for i in range(self.data[self.data["state"]]["index"]):
            self.sprite.append(pygame.image.load(self.folder + "sprite/" + self.data["state"] + "/sprt" + str(i) + ".png").convert_alpha())
        #---end for---
        self.updatePictureSize()
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
        self.walking = {"right" : False, "left" : False}
        self.jump = {"jump" : False, "fastfall" : False}
    #---end init---

    def updatePlayerInput(self, inp, running = False):
        self.walking["right"] = inp["right"][0]
        self.walking["left"] = inp["left"][0]
        self.jump["jump"] = inp["up"][0]
        if self.walking["right"] == True and self.walking["left"] == True:
            self.walking = {"right" : False, "left" : False}
            self.inptime = 0
        elif self.walking["right"] == True or self.walking["left"] == True:
            self.inptime += 1
            if self.walking["right"] == True :
                self.changeState("backward")
            elif self.walking["left"] == True :
                self.changeState("foward")
        else:
            self.inptime = 0
        #---end if---
    #---end updateWalking---

    def changeState(self, state, dead = 0):
        super().changeState(dead)
        if not(dead):
            self.data["newState"] = state
        #---end if---
    #---end changeState---
#---end player---  