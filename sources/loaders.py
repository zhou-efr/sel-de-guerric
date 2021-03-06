"""loader.py

    it's the file containing all the loaders class and their needed functions

"""
import pygame
import objects as o
import backendFunctions as b

class environmentLoader:
    """environment loader is the class which load and keep all the needed features communal to all the environment

        current features loaded:
            items
            levels
            >> beasts
    """
    def __init__(self, surface, environment, level = 1, area = 11):
        #attributs settings
        self.environment = environment
        self.folder = "../files/environment" + str(environment) + "/"
        self.windowData = {"width" : surface.get_rect().right, "height" : surface.get_rect().bottom, "sizeOfTiles": int(surface.get_rect().right/16)}
        self.currentLevel = levelLoader(environment, level, self.windowData["sizeOfTiles"], area)

        #initialazation
        self.sizeUpdate(self.windowData["sizeOfTiles"])
        self.currentLevel.currentBoard.resizeBackground((self.windowData["width"],self.windowData["height"]))
    #---end init--

    def nextLevel(self):
        self.currentLevel = levelLoader(self.environment, self.currentLevel.getLevel()+1, self.windowData["sizeOfTiles"])
    #---end nextLevel---

    def sizeUpdate(self, size):
        for i in self.getObjects():
            i.updateObjectPictureSize(size)
        #---end for---

        for i in self.getEntities():
            i.updatePictureSize(size)
    #---end sizeUpdate---

    def levelChanged(self):      
        if self.getPlayer().BoardChanged != None :
            self.currentLevel.boardChange(self.getPlayer().BoardChanged)
            if self.currentLevel.position == 100:
                quit()
            #---end if---
            self.getPlayer().BoardChanged = None
            return True
        #---end if---
        return False
    #---end levelChanged---

    #---Beginning accessor---
    def getPlayer(self):
        return self.currentLevel.currentBoard.entities[0]

    def getRect(self):
        return self.currentLevel.currentBoard.rect

    def getYcollideRects(self):
        return self.currentLevel.currentBoard.collidesRect

    def getBackground(self):
        return self.currentLevel.currentBoard.getBackground()

    def getEntities(self):
        return self.currentLevel.currentBoard.entities

    def getAllEntities(self):
        return self.currentLevel.currentBoard.entities + self.currentLevel.currentBoard.zone["ent"]

    def getWidth(self):
        return self.currentLevel.currentBoard.boardata["width"]
    
    def getHeight(self):
        return self.currentLevel.currentBoard.boardata["height"]

    def getObjects(self):
        return self.currentLevel.currentBoard.item

    def getAllObjects(self):
        return self.currentLevel.currentBoard.item + self.currentLevel.currentBoard.zone["obj"]

    def getZones(self):
        return self.currentLevel.currentBoard.zone

    def getFolder(self):
        return self.folder

    def getLevel(self):
        return self.currentLevel

    def getBoard(self):
        return self.currentLevel.currentBoard

    def getEnvironment(self):
        return self.environment
    #---End of accessors---
#---end environmentLoader---

class levelLoader:
    """this class load a level
        it's mean it's load :
            the musique
            the layout of each area
        
        and it's contain :
            loaded adress
            layout array
            the player data (maybe yes, maybe no it's depends on the backend structure)

        and has methode :
            for change area (in function of direction 'n' 's' 'e' 'o')
            accessors
    """
    def __init__(self, environment, level, sizeOfTiles, area = 11):
        #setting internal variables
        self.environment = environment
        self.level = level
        self.folder = "../files/environment" + str(environment) + "/level" + str(level)
        self.musicAdress = self.folder + "soundtrack.mp3"
        self.levelStructureAdress = self.folder + "/levelStruct.txt"
        self.levelStructure = []
        self.position = area #11 being the starting board
        self.player = None
        self.currentBoard = areaLoader(self.environment, self.level, self.position)
        self.sizeOfTiles = sizeOfTiles
        #initialazation
        if self.currentBoard.list[0] == []:
            self.currentBoard.list[0].append(o.player())
            if self.player != None:
                self.currentBoard.list[0][0].position["x1"] = self.player["x1"]
                self.currentBoard.list[0][0].position["x2"] = self.player["x2"]
                self.currentBoard.list[0][0].position["y1"] = self.player["y1"]
                self.currentBoard.list[0][0].position["y2"] = self.player["y2"]
            #---end if---
        #---end if---
        self.currentBoard.init_in_level()
        self.initStructure()
        self.sizeUpdate(self.sizeOfTiles)
        self.currentBoard.resizeBackground((self.sizeOfTiles*16,self.sizeOfTiles*9))
    #---end init--

    def sizeUpdate(self, size):
        for i in self.currentBoard.item:
            i.updateObjectPictureSize(size)
        #---end for---

        for i in self.currentBoard.entities:
            i.updatePictureSize(size)
    #---end sizeUpdate---

    def initStructure(self):
        #board initialazation
        contents = None 

        try:
            with open(self.levelStructureAdress, 'r', encoding='utf-8') as file:
                contents = file.read().split('\n')
            #---end with---
            
            for i in range(len(contents)):
                contents[i] = contents[i].split()
                for j in range(len(contents[i])):
                    contents[i][j] = int(contents[i][j])
                #---end for---
            #---end for---

            self.levelStructure = contents
            
        except FileNotFoundError as er:
            print("file not found ", er)
        #---end try---
    #---end initStructure---

    def boardChange(self, data):
        self.position = data.area
        self.player = {"x1":0, "x2":0, "y1":0, "y2":0}
        self.player["x1"] = data.x
        self.player["x2"] = data.x
        self.player["y1"] = data.y
        self.player["y2"] = data.y
        
        self.currentBoard = areaLoader(self.environment, self.level, self.position)
        if data.force == 'True':
            while len(self.currentBoard.list[0]) != 0:
                del(self.currentBoard.list[0][0])
            #---end while---
        #---end if---

        self.currentBoard.list[0].append(o.player())
        self.currentBoard.list[0][-1].position["x1"] = self.player["x1"]
        self.currentBoard.list[0][-1].position["x2"] = self.player["x2"]
        self.currentBoard.list[0][-1].position["y1"] = self.player["y1"]
        self.currentBoard.list[0][-1].position["y2"] = self.player["y2"]
        
        while len(self.currentBoard.list[0]) > 1:
            del(self.currentBoard.list[0][1])
            self.player = None
        #---end while---

        self.currentBoard.init_in_level()
        self.sizeUpdate(self.sizeOfTiles)
        self.currentBoard.resizeBackground((self.sizeOfTiles*16,self.sizeOfTiles*9))

        # Must do a security to not go out of the level structure, but i'm lazy right now
        #I assume it was at something like 1 AM
    #---end boardChange---

    def respawn(self):
        if self.currentBoard.list[0][0].data["state"] == "dead":
            self.currentBoard = areaLoader(self.environment, self.level, self.position)
            if self.player != None:
                while len(self.currentBoard.list[0]) > 0:
                    del(self.currentBoard.list[0][0])
                #---end while---
                self.currentBoard.list[0].append(o.player())
                self.currentBoard.list[0][0].position["x1"] = self.player["x1"]
                self.currentBoard.list[0][0].position["x2"] = self.player["x2"]
                self.currentBoard.list[0][0].position["y1"] = self.player["y1"]
                self.currentBoard.list[0][0].position["y2"] = self.player["y2"]
            #---end if---
            if self.currentBoard.list[0] == []:
                self.currentBoard.list[0].append(o.player())
                if self.player != None:
                    self.currentBoard.list[0][0].position["x1"] = self.player["x1"]
                    self.currentBoard.list[0][0].position["x2"] = self.player["x2"]
                    self.currentBoard.list[0][0].position["y1"] = self.player["y1"]
                    self.currentBoard.list[0][0].position["y2"] = self.player["y2"]
                # ---end if---
            # ---end if---
            self.currentBoard.init_in_level()
            self.initStructure()
            self.sizeUpdate(self.sizeOfTiles)
            self.currentBoard.resizeBackground((self.sizeOfTiles * 16, self.sizeOfTiles * 9))
            return True
        else:
            return False
        #---end if---
    #---end respawn---

    #---Beginning of accessors---
    def getBoard(self):
        return self.currentBoard

    def setBoard(self, position):
        self.currentBoard = areaLoader(self.environment, self.level, position)

    def getfolder(self):
        return self.folder

    def getLevel(self):
        return self.level

    def getStructure(self):
        return self.levelStructure

    def getStructureAdress(self):
        return self.levelStructureAdress

    def getPosition(self):
        return self.position

    def getMusic(self):
        return self.musicAdress

    def getEnvironment(self):
        return self.environment
    #---end of accessors---
#---end levelLoader---       

class areaLoader:
    """area loader is the class containing all the necessary contained in folders


        image folder achitexture (c'est des fichier text xD)
        |
        ├environment0
        |   ├level 0
        |   |   ├board00.dat
        |   |   ├board10.dat
        |   |   ├board01.dat
        |   |   ├etc
        |   ├level 1
        |   |   ├board00.dat
        |   |   ├board10.dat
        |   |   ├board01.dat
        |   |   ├etc
        |   ├etc
        ├environment01
        |   ├etc
        ├etc

        level achitecture (the index of txt files)
        11 12 13 14
        21 22 23 24
        31 32 33 34 99
        41 42 43 44
        
        the player always spawn at board's index 00 and the arival board is always index 99
    """


    def __init__(self,environment, level, board):
        #setting internal variables
        self.environment = environment
        self.level = level 
        self.board = board
        self.adress = "../files/environment" + str(environment) + "/level" + str(level) + "/" + str(self.board)
        self.boardAdress = str(self.adress) + "/board.dat"
        self.backAdress = str(self.adress) + "/back.png"
        self.background = pygame.image.load(self.backAdress)
        self.boardata = fileLoader(self.adress, "/data.dat")
        self.list = b.list(self)
        self.rect = pygame.Rect(0,0,self.boardata["width"], self.boardata["height"])
        self.collidesRect = [pygame.Rect(0,0,self.boardata["width"], 0),pygame.Rect(0,self.boardata["height"]-4,self.boardata["width"], 4)]
    #---end init---

    def init_in_level(self):
        self.simpleList = b.simpleList(self)
        self.entities = self.simpleList[0]
        self.item = self.simpleList[1]
        self.zone = self.simpleList[2]

        for e in self.item:
            if isinstance(e, o.entities):
                e.stateUpdater(self.item, self)
            else:
                b.wallUpdater(e, self.item, self)
            #---end if---
        #---end for---
    #---end init_in_level---

    #---Beginning of accessors---
    def getBackAdress(self):
        return self.backAdress

    def getBoardAdress(self):
        return self.boardAdress

    def getBackground(self):
        return self.background
    
    def resizeBackground(self, size):
        self.background = pygame.transform.scale(self.background, size)

    def getAdress(self):
        return self.adress

    def getLevel(self):
        return self.level

    def getEnvironment(self):
        return self.environment
    
    def getSimpleList(self):
        return self.simpleList

    def getList(self):
        return self.list
    #---End of accessors---
#---end AreaLoader---

def strToArray(text):
    arrayProduce = []
    for i in text:
        arrayProduce.append(i)
    #---end for---
    return arrayProduce
#--end strToArray---

def fileLoader(folderRoot, file = ""):
    """recursively convert a txt file into a dictionnary"""
    data = {}
    contents = []
    root = folderRoot + file
    with open(root, 'r') as target:
        contents = target.read().split("\n")
    #---end with---
    for i in range(len(contents)):
        contents[i] = contents[i].split()
        try:
            contents[i][1] = eval(contents[i][1])
        except NameError:
            contents[i][1] = str(contents[i][1])
            if(contents[i][1] == "subDictionnary"):
                contents[i][1] = fileLoader(folderRoot, contents[i][0] + ".dat")
            #---end if---
        #---end try---
        data[contents[i][0]] = contents[i][1]
    #---end for---
    return data
#---end fileLoader---