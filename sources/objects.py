"""object.py
    this file contain all objects needed
    for instance:
        items

author : la tribut des zhou
"""
import pygame

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
    #---end init---

    #---beginning accessors
    def getKeyChar(self):
        return self.keyChar
    
    def getPictureAdress(self):
        return self.pictureAdress
    
    def getPicture(self):
        return self.picture
    #---end accessors---

class entities (item):

    def __init__(self, keyChar, environment):
        super().__init__(keyChar, environment)
        self.info = "./files/environment" + str(environment)+"/" + keyChar + "/" + keyChar + ".dat"
        self.folder = "./files/environment" + str(environment)+"/" + keyChar + "/"
        self.data = {}
        self.sprite = []
        self.internalClock = -1
        contents = []
        try:
            with open(self.info, 'r') as target:
                contents = target.read().split("\n")
            #---end with---

            for i in range(len(contents)):
                contents[i] = contents[i].split()
                subContents = []
                try:
                    contents[i][1] = eval(contents[i][1])
                    if contents[i][1] < 0:
                        contents[i][1] = {}
                        try:
                            root = self.folder + "sprite/" + contents[i][0]  + "/" + contents[i][0] + ".dat"
                            with open(root , 'r') as target:
                                subContents = target.read().split("\n")
                            #---end with---

                            for j in range(len(contents)):
                                subContents[j] = subContents[j].split()
                                try:
                                    subContents[j][1] = eval(subContents[j][1])
                                except NameError as identifier:
                                    subContents[i][1] = str(subContents[i][1])
                                #---end try---
                                contents[i][1][subContents[j][0]] = subContents[j][1]
                            #---end for---
                        except (FileNotFoundError, IndexError) as identifier:
                            print(identifier)
                        #---end try---
                    #---end if---
                except NameError as identifier:
                    contents[i][1] = str(contents[i][1])
                self.data[contents[i][0]] = contents[i][1]
            #---end for---
        except (FileNotFoundError, IndexError) as identifier:
            print(identifier)
            self.data = {"sprite" : 1, "x" : 2.0, "y" : 2.0}
        #---end try---
        
        self.updateSprite()
    #---end init---

    def internalClockUpdate(self):
        if (self.internalClock >= (self.data[self.data["state"]]["index"] - 1)):
            self.internalClock = -1
        #---end if---
        self.internalClock += 1
    #--end iternalClockUpdate---

    def getPicture(self):
        self.internalClockUpdate()
        return self.sprite[self.internalClock]
    #---end getPicture---

    def getPosition(self):
        return self.data["x"], self.data["y"]
    #---end getPosition---

    def updateSprite(self):
        for i in range(self.data[self.data["state"]]["index"]):
            self.sprite.append(pygame.image.load(self.folder + "sprite/" + self.data["state"] + "/sprt" + str(i) + ".png").convert_alpha())
        #---end for---
    #---end updateSprite---

    def changeState(self, dead = 0):
        if dead:
            self.data["state"] = "dead"
        #---end if---
        
        self.updateSprite()
    #---end changeState---
#---end entities---

class player (entities):

    def __init__(self):
        super().__init__('p', 0)
    #---end init---

    def changeState(self, dead = 0):
        if self.data["state"] == "bouncing" :
            self.data["state"] = "static"
        elif self.data["state"] == "static":
            self.data["state"] = "bouncing"
        #---end if---
        
        if dead:
            self.data["state"] = "dead"
        #---end if---
        
        self.updateSprite()
    #---end changeState---
#---end player---  