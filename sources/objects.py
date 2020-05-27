"""object.py
    this file contain all objects needed
    for instance:
        items

author : la tribut des zhou
"""
import pygame
import backendFunctions as b
import math as m
import loaders as l
import random as r
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
        self.folder = "../files/environment" + str(environment) + "/items/" + keyChar + "/"
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
#---end item---

class multipleItem(item):
    """docstring for multipleItem"""
    def __init__(self, keyChar, environment):
        super(multipleItem, self).__init__()
        self.keyChar = keyChar
        self.environment = environment
        self.data = {};
        self.dataFolder = self.folder + "data/"
        try:
            self.data = fileLoader(self.dataFolder, str(keyChar)+".dat");
        except FileNotFoundError as e:
            print(e)
            exit(-1);
        #---end try---

    def loadPicture(self):
        self.data["picture"] = []
        for i in range(self.data["sizeX"]):
            self.data["picture"].append([])
            for int in range(self.data["sizeY"]):
                self.data["picture"][i].append(pygame.image.load(str(i)+str(j)))
            #---end for---
        #---end for---
    #---end loadPicture---

    def updateObjectPictureSize(self, size = 120):
        for i in range(self.data["sizeX"]):
            for j in range(self.data["sizeY"]):
                self.data["picture"][i][j] = pygame.transform.scale(self.data["picture"][i][j].convert_alpha(), (size, size))
            #---end for---
        #---end for---
    #---end updatePictureSize---

    def getPicture(self, coordinate):
        return self.data["picture"][coordinate[0]][coordinate[1]]
    #---end getPicture---

#---end multipleItem---



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
        self.globalfolder = self.folder
        self.folder = self.globalfolder + "sprite/" + self.data["state"] + "/"

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

    def stateUpdater(self, lists, world):
        pass
    #---end stateUpdater---

    def getPicture(self):
        if self.changed and self.data[self.data["state"]]["initialState"] == self.internalClock:
            self.data["state"] = self.data["newState"]
            self.folder = self.globalfolder + "sprite/" + self.data["state"] + "/"
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
            self.sprite.append(pygame.image.load(self.folder + "sprt" + str(i) + ".png").convert_alpha())
        #---end for---
        self.updatePictureSize(self.size)
    #---end updateSprite---

    def changeState(self, state = "default", dead = 0):
        self.data["newState"] = state
        if dead:
            self.data["state"] = "dead"
        else:
            self.data["newState"] = state
            self.changed = True
        #---end if---
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
        self.cdw = {"walljump": True, "jump": True, "action": True, "double_jump": "False"}
        self.rice = 1000
        self.coef = 2
        self.ricesize = "high"
        self.bounce = False
        self.BoardChanged = None
    #---end init---

    def updatePlayerInput(self, inp, running = False):
        self.walking["right"] = inp["right"][0]
        self.walking["left"] = inp["left"][0]
        self.jump["jump"] = inp["up"][0]
        self.jump["fastfall"] = inp["down"][0]

        if inp["action1"][0]:
            if self.cdw["action"] == True:
                if self.cdw["action"]:
                    self.cdw["action"] = False
                    self.bounce = True
                #---end if---
            #---end if---
        else:
            self.cdw["action"] = True
        #---end if---

        if self.bounce:
            if self.state == "bouncing" and self.cdw["double_jump"] == "False":
                self.cdw["double_jump"] = "True"
            if self.hit["floor"]:
                self.bounce = False
                if self.state == "bouncing":
                    self.state = "default"
                else:
                    self.state = "bouncing"
                #---end if---
            #---end ifs---
        #---end if---

        if self.state == "bouncing" and self.cdw["double_jump"] == "False":
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
            elif self.cdw["double_jump"] == "True":
                self.changeState("double_jump")
            elif self.hit["rwall"] and self.cdw["walljump"]:
                self.changeState("rwall_jump")
            elif self.hit["lwall"] and self.cdw["walljump"]:
                self.changeState("lwall_jump")
            #---end if---
        #---end if--- 

        self.rice -= (self.speed["x"]**2 + self.speed["y"]**2)**(1/2)**self.coef
        if self.rice >= 750:
            self.ricesize = "high"
        elif self.rice > 250:
            self.ricesize = "normal"
        elif self.rice > 0:
            self.ricesize = "low"
        else:
            self.changeState("dead")
        #---end if---
    #---end updatePlayerInput---
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
        for s in board.list[7]:
            if (self.position["x1"]-0.2 <= s.position["x1"] <= self.position["x1"]+0.2 or self.position["x2"]-0.2 <= s.position["x2"] <= self.position["x2"]+0.2) and (self.position["y1"]-0.2 <= s.position["y1"] <= self.position["y1"]+0.2 or self.position["y2"]-0.2 <= s.position["y2"] <= self.position["y2"]+0.2) and self.hit["floor"]:
                self.spot = s
                self.position["x1"] = s.position["x1"]
                self.position["x2"] = s.position["x2"]
                self.position["y1"] = s.position["y1"]
                self.position["y2"] = s.position["y2"]
            elif self.state == 'ground':
                if s.position["x1"] < self.position["x1"] and s.position["x2"] < self.position["x2"] and self.position["y2"] >= s.position["y1"] and (self.r_spot == None or s.position["x1"] < self.r_spot.position["x1"]):
                    self.l_spot = s
                elif s.position["x1"] > self.position["x1"] and s.position["x2"] > self.position["x2"] and self.position["y2"] >= s.position["y1"] and (self.r_spot == None or s.position["x1"] > self.r_spot.position["x1"]):
                    self.r_spot = s
                #---end if---
            elif s.position["x1"] < self.position["x1"] and s.position["x2"] < self.position["x2"] and (self.r_spot == None or (s.position["x1"]**2 + s.position["y1"]**2)**(1/2) < (self.position["x1"]**2 + self.position["y1"]**2)**(1/2)):
                self.l_spot = s
            elif s.position["x1"] > self.position["x1"] and s.position["x2"] > self.position["x2"] and (self.r_spot == None or (s.position["x1"]**2 + s.position["y1"]**2)**(1/2) < (self.position["x1"]**2 + self.position["y1"]**2)**(1/2)):
                self.r_spot = s
            #---end if---
        #---end for---
    #---end sdetector---

    def stateUpdater(self, lists, world):
        if self.state != 'dead':
            self.sdetector(world.getBoard())
            if self.spot != None:
                self.changeState('default')
                self.state = 'default'
            if self.state == "default":
                self.rjump = int(r.random() * 50)
                if ((lists[0].position["x1"]-self.position["x1"])**2 + (lists[0].position["y1"]-self.position["y1"])**2)**(1/2) <= self.view:
                    self.state = 'attack'
                    if lists[0].position["x1"] < self.position["x1"]:
                        self.changeState('attack_left')
                    else:
                        self.changeState('attack_right')
                    #---end if---
                elif self.rjump == 0 and self.r_spot != None:
                    self.changeState('go_right')
                    self.state = 'jump'
                elif self.rjump == 1 and self.l_spot != None:
                    self.changeState('go_left')
                    self.state = 'jump'
                #---end if---
            elif self.hit["floor"] and self.spot == None:
                self.state = 'ground'
                if self.r_spot != None and self.l_spot != None:
                    distr = self.position["x1"]-self.r_spot.position["x1"]
                    distl = self.position["x1"]-self.l_spot.position["x1"]
                    if (distr < distl or (self.position["y1"] < self.l_spot.position["y1"]) and self.position["y1"] >= self.r_spot.position["y1"]):
                        self.changeState('ground_right')
                    elif (distr < distl or (self.position["y1"] < self.l_spot.position["y1"]) and self.position["y1"] >= self.r_spot.position["y1"]):
                        self.changeState('ground_left')
                    else:
                        self.changeState('ground')
                    #---end if---
                elif self.r_spot != None:
                    self.changeState('ground_right')
                elif self.l_spot != None:
                    self.changeState('ground_left')
                else:
                    self.changeState('ground')
                #---end if---
            if lists[0].position["y2"] == self.position["y1"]+1 and (lists[0].position["x1"] <= self.position["x1"] <= lists[0].position["x2"]+1 or self.position["x1"] <= lists[0].position["x1"] <= self.position["x2"]+1):
                self.changeState('dead')
                self.state = 'dead'
            #---end if---
        #---end if---
    #---end stateUpdater---
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
        super().__init__(self, keyChar, environment)
        self.territory = None
        self.max = None
        self.min = None
        self.retract = False
        self.rmove = 0
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
            if self.state != 'afraid':
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

    def stateUpdater(self,lists, world):
        if item.state != 'dead':
            if self.inptime >= 100:
                self.state = 'default'
                self.changeState('default')
                self.inptime = 0
            elif lists[0].position["y2"] == self.position["y1"]+1 and (lists[0].position["x1"] <= self.position["x1"] <= lists[0].position["x2"]+1 or self.position["x1"] <= lists[0].position["x1"] <= self.position["x2"]+1) or self.state == 'afraid':
                self.state = 'afraid'
                if self.speed["x"] > 0:
                    self.changeState('afraid_right')
                else:
                    self.changeState('afraid_left')
                #---end if---
                self.inptime += 1
            elif self.territory["x1"] <= lists[0].position["x1"] <= self.territory["x2"] and  self.territory["y1"] <= lists[0].position["y1"] <= self.territory["y2"] or self.state == 'attack':
                self.state = 'attack'
                if self.speed["x"] > 0:
                    self.changeState('attack_right')
                else:
                    self.changeState('attack_left')
                #---end if---
                self.inptime += 1
            elif self.state == 'default':
                self.rmove = int(r.random()*75)
                if self.rmove == 1:
                    self.changeState('go_left')
                    self.state = 'move'
                elif self.rmove == 2:
                    self.changeState('go_right')
                    self.state = 'move'
                #---end if---
            else:
                self.inptime += 1
            #---end if
        #---end if---
    #---end stateUpdater---
#---end rat---

class trash(entities):
    """docstring for trash"""
    def __init__(self, keyChar, environment, x1, x2, y1, y2):
        super(trash, self).__init__(keyChar, environment)
        self.keyChar = keyChar
        self.environment = environment
        self.position["x1"] = x1
        self.position["x2"] = x2
        self.position["y1"] = y1
        self.position["y2"] = y2
    #---end init---

    def stateUpdater(self, entities, world):
        if self.data["state"] != "dead" and entities[0].data["state"] != "dead":
            #print("trash : (", self.position["x1"], ",", self.position["x1"] , ") " , "player : (",  entities[0].position["x1"], ",", entities[0].position["x1"] , ") ")
            if self.position["x1"] < entities[0].position["x1"] < self.position["x2"]+1 or self.position["x1"] < entities[0].position["x2"]+1 < self.position["x2"]+1:
                if self.position["y1"] == entities[0].position["y1"]-1:
                    entities[0].changeState("dead", True)
                    self.data["state"] = "static"
                elif self.position["y1"] <= entities[0].position["y1"]-1 and self.hit["floor"]:
                    self.data["state"] = "jump"
                else:
                    self.data["state"] = "static"
                #---end if---
            #---end if---
        #---end if---
    #---end stateUpdater---
#---end trash---

class exit(item):
    def __init__(self, keyChar, environment) :
        super().__init__(keyChar, environment)
        self.area = 11
        self.x = 1
        self.y = -1
        self.force = 'False'
    #---end init---

    def playerExit(self, player):
        if (self.position["x1"] <= player.position["x1"] <= self.position["x2"] or player.position["x1"] <= self.position["x1"] <= player.position["x2"]) and (self.position["y1"] >= player.position["y1"] >= self.position["y2"] or player.position["y1"] >= self.position["y1"] >= player.position["y2"]):
            player.BoardChanged = self
        #---end if---
    #---end playerExit---
#---end exit---