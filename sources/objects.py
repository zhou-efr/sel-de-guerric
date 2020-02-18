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
    #---end init---
#---end entities---

class player (entities):

    def __init__(self):
        self.spriteAdress = "./files/player/sprite/sprt"
        self.info = "./files/player/p.dat"
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
                try:
                    contents[i][1] = eval(contents[i][1])
                except NameError as identifier:
                    contents[i][1] = str(contents[i][1])
                self.data[contents[i][0]] = contents[i][1]
            #---end for---
        except (FileNotFoundError, IndexError) as identifier:
            print(identifier)
            self.data = {"sprite" : 1, "x" : 2.0, "y" : 2.0}
        #---end try---

        for i in range(self.data["sprite"]):
            self.sprite.append(pygame.image.load(self.spriteAdress + str(i) + ".png"))
        #---end for---
        


    #---end init---

    def getPicture(self, clock = 0):
        if (clock%(self.data["sprite"]) == 0):
            self.internalClock = -1
        #---end if---

        self.internalClock += 1

        return self.sprite[self.internalClock]
    #---end getPicture---

    def getPosition(self):
        return self.data["x"], self.data["y"]
    
#---end player---