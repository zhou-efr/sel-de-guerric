import pygame

pygame.init()

def strToArray(text):
    arrayProduce = []
    for i in text:
        arrayProduce.append(i)
    #---end for---
    return arrayProduce
#--end strToArray---

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

    def __init__(self, environment, level):
        #setting internal variables
        self.environment = environment
        self.level = level
        self.folder = "C:/Users/gundamzhou/Documents/GitHub/sel-de-guerric/files/environment" + str( environment) + "/level" + str( level)
        self.musicAdress = self.folder + "soundtrack.mp3"
        self.levelStructureAdress = self.folder + "levelStruct.txt"
        self.levelStructure = []
        self.position = 11
        self.currentBoard = areaLoader(self.environment, self.level, 11) #11 being the starting board

        #initialazation
        self.initStructure()
    #---end init---

    def initStructure(self):
        #board initialazation
        contents = None 

        try:
            with open(self.levelStructureAdress, 'r') as file:
                contents = file.read().split('\n')
            #---end with---

            for i in range(len(contents)):
                contents[i] = strToArray(contents[i])
            #---end for---

            self.levelStructure = contents
            
        except FileNotFoundError:
            print("file not found")
        #---end try---
    #---end initStructure---

    def boardChange(self, direction):
        if (direction == 'n'):
            self.position += 1
        elif (direction == 's'):
            self.position -= 1
        elif (direction == 'o'):
            self.position += 10
        elif (direction == 'e'):
            self.position -= 10
        else:
            self.position += 0

        self.currentBoard = areaLoader(self.environment, self.level, 11)
        

class areaLoader:
    """area loader is the class containing all the necessary contained in folders


    image folder achitexture (c'est des fichier text xD)
    |
    ├environment0
    |   ├level 0
    |   |   ├board00.txt
    |   |   ├board10.txt
    |   |   ├board01.txt
    |   |   ├etc
    |   ├level 1
    |   |   ├board00.txt
    |   |   ├board10.txt
    |   |   ├board01.txt
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
        self.adress = "C:/Users/gundamzhou/Documents/GitHub/sel-de-guerric/files/environment" + str( environment) + "/level" + str( level)
        self.boardAdress = self.adress + "/board" + self.board + ".txt"
        self.backAdress = self.adress + "/back" + self.board + ".png"
        self.area = []

        #beginning of initialazation 
        self.initBoard()
    #---end init---

    def initBoard(self):
        #board initialazation
        contents = None 

        try:
            with open(self.adress, 'r') as file:
                contents = file.read().split('\n')
            #---end with---

            for i in range(len(contents)):
                contents[i] = strToArray(contents[i])
            #---end for---

            self.area = contents
            
        except FileNotFoundError:
            print("file not found")
        #---end try---
    #---end initBoard---

    def getBackAdress(self):
        return self.backAdress

    def getBoardAdress(self):
        return self.boardAdress

    def getAdress(self):
        return self.adress

    def getLevel(self):
        return self.level

    def getArray(self):
        return self.area

    def getEnvironment(self):
        return self.environment
#---end AreaLoader---


def areaPrinter(surface, board, environment):
    """
        surface : a pygame surface
        board : 2d array containing keyChar
        environment : environment object 
    """
#---end areaPrinter---

print(areaLoader(1,1,1))