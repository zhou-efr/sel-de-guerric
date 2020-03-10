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
        if type(self) == item:
            self.pictureAdress = self.folder + self.state + ".png"
            self.picture = pygame.image.load(self.pictureAdress)
        #---end if---
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
        self.hit = {"rwall": False, "lwall": False, "floor": False, "ceil": False}
        self.speed = {"x" : 0,"y" : 0}
        self.acceleration = {"x" : 0,"y" : 0}
        self.inptime = 0
        self.vXMax = 1
        self.vYMax = 1
        self.size = 120
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

    def updatePictureSize(self, size):
        self.size = size
        for i in range(len(self.sprite)):
            self.sprite[i] = pygame.transform.scale(self.sprite[i].convert_alpha(), (self.size, self.size))
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
        self.updatePictureSize( self.size)
    #---end updateSprite---

    def changeState(self, state = "default", dead = 0):
        if dead:
            self.data["state"] = "dead"
        #---end if---
        self.changed = True
        if not(dead):
            self.data["newState"] = state
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
        self.inptime = 1
        self.cdw = {"walljump": True, "jump": True, "action": True}
        self.rice = 100
        self.coef = 0.1
        self.ricesize = "high"
    #---end init---

    def updatePlayerInput(self, inp, running = False):
        self.walking["right"] = inp["right"][0]
        self.walking["left"] = inp["left"][0]
        self.jump["jump"] = inp["up"][0]
        self.jump["fastfall"] = inp["down"][0]

        if inp["action1"][0]:
            if self.cdw["action"]:
                self.cdw["action"] = False
                if self.state == "bouncing":
                    self.state = "default"
                    self.cdw["double_jump"] = True
                else:
                    self.state = "bouncing"
                #---end if---
            #---end if---
        elif self.hit["floor"]:
            self.cdw["action"] = True
        #---end if---


        if self.state == "bouncing":
            self.jump["jump"] = True
            self.jump["fastfall"] = False
        #---end if---

        if self.walking["right"] == True and self.walking["left"] == True:
            self.walking = {"right" : False, "left" : False}
        if self.walking["right"] == False and self.walking["left"] == False:
            if self.data["state"] == "backward" or self.data["state"] == "staticb":
                self.changeState("staticb")
            else:
                self.changeState("static")
            #---end if---
        elif self.walking["right"] == True or self.walking["left"] == True:
            if self.walking["right"] == True :
                self.changeState("backward")
            elif self.walking["left"] == True :
                self.changeState("foward")
            #---end if---
        #---end if---

        if self.jump["fastfall"] and not(self.hit["floor"]):
            self.changeState("fastfall")
        elif self.data["state"] == "fastfall" and self.hit["floor"]:
            self.changeState("static")
        #---end if---
        
        if self.jump["jump"] and self.jump["fastfall"]:
            self.jump = {"jump": False, "fastfall": False}
        elif self.hit["floor"]:
            self.inptime = 1
        elif self.jump["jump"]:
            if self.inptime < 10:
                self.inptime += 1
            #---end if---
        else:
            self.inptime = 1
        #---end if---

        if self.jump["jump"]:
            if self.hit["floor"]:
                self.changeState("floor_jump")
            elif self.cdw["double_jump"]:
                self.changeState("double_jump")
            elif self.hit["rwall"] and self.cdw["walljump"]:
                self.changeState("rwall_jump")
            elif self.hit["lwall"] and self.cdw["walljump"]:
                self.changeState("lwall_jump")
            #---end if---
        #---end if--- 

        self.rice -= (self.speed["x"]**2 + self.speed["y"]**2)**(1/2) * self.coef
        if self.rice >= 75:
            self.ricesize = "high"
        elif self.rice > 25:
            self.ricesize = "normal"
        elif self.rice > 0:
            self.ricesize = "low"
        else:
            self.changeState("dead")
        #---end if--- 
    #---end updateWalking---
#---end player--- 

class fish(entities):

    def __init__(self, keyChar, board):
        super().__init__(keyChar, 0)
        self.rjump = 2
        self.r_spot = None
        self.l_spot = None
        self.spot = None
        self.view = 5
    #---end init---

    def sdetector(self, board):
        self.l_spot = None
        self.r_spot = None
        self.spot = None
        for s in board.list[6]:
            if (self.position["x1"]-0.5 <= s.position["x1"] <= self.position["x1"]+0.5 or self.position["x2"]-0.5 <= s.position["x2"] <= self.position["x2"]+0.5) and (self.position["y1"]-0.5 <= s.position["y1"] <= self.position["y1"]+0.5 or self.position["y2"]-0.5 <= s.position["y2"] <= self.position["y2"]+0.5) and self.hit["floor"]:
                self.spot = s
                self.position["x1"] = s.position["x1"]
                self.position["x2"] = s.position["x2"]
                self.position["y1"] = s.position["y1"]
                self.position["y2"] = s.position["y2"]
            elif s.position["x1"] < self.position["x1"] and s.position["x2"] < self.position["x2"] and (self.r_spot == None or s.position["x1"] < self.r_spot.position["x1"]):
                self.l_spot = s
            elif s.position["x1"] > self.position["x1"] and s.position["x2"] > self.position["x2"] and (self.r_spot == None or s.position["x1"] > self.r_spot.position["x1"]):
                self.r_spot = s
            #---end if---
        #---end for---
    #---end sdetector---
#---end fish---

class zrat(item):


    def __init__(self, keyChar, environment):
        super().__init__(self, keyChar, environment)
        self.min = None
        self.max = None
    #---end init---
#---end zrat---

class rat(entities):

    def __init__(self, keyChar, environment):
        super().__init__(keyChar, environment)
        self.territory = None
        self.max = None
        self.min = None
        self.retract = False
    #---end init---

    def updateTerritory(self, board):
        if self.territory == None:
            for z in board.list[7]:
                if (self.position["x1"] <= z.min["x1"] <= self.position["x1"]+1 or z.position["x1"] <= self.min["x1"] <= z.position["x1"]+1) and (self.position["y1"] <= z.min["y1"] <= self.position["y1"]+1 or z.position["y1"] <= self.min["y1"] <= z.position["y1"]+1):
                    self.territory = z.min
                    self.min = z.min
                    self.max = z.max
                #---end if---
            #---end for---
        else:
            if self.state == 'default':
                self.territory["x1"] -= 0.025
                self.territory["x2"] += 0.025
                self.territory["y1"] += 0.025
                self.territory["y2"] -= 0.025
                if self.territory["x1"] < self.max["x1"]:
                    self.territory["x1"] = self.max["x1"]
                if self.territory["x2"] > self.max["x2"]:
                    self.territory["x2"] = self.max["x2"]
                if self.territory["y1"] > self.max["y1"]:
                    self.territory["y1"] = self.max["y1"]
                if self.territory["y2"] < self.max["y2"]:
                    self.territory["y2"] = self.max["y2"]
                #---end ifs---
            elif self.retract:
                self.retract = False
                self.territory["x1"] += 1
                self.territory["x2"] -= 1
                self.territory["y1"] -= 1
                self.territory["y2"] += 1
                if self.territory["x1"] > self.min["x1"]:
                    self.territory["x1"] = self.min["x1"]
                if self.territory["x2"] < self.min["x2"]:
                    self.territory["x2"] = self.min["x2"]
                if self.territory["y1"] < self.min["y1"]:
                    self.territory["y1"] = self.min["y1"]
                if self.territory["y2"] > self.min["y2"]:
                    self.territory["y2"] = self.min["y2"]
                #---end ifs---
            #---end if---
        #---end if---
    #---end updateTerritory---
#---end rat---
