"""loader.py

    it's the file containing all the loaders class and their needed functions

"""
import objects as o

class environmentLoader:
    """environment loader is the class which load and keep all the needed features communal to all the environment

        current features loaded:
            items
            levels
            >> beasts
    """
    def __init__(self, environment, level = 1, area = 11):
        #attributs settings
        self.environment = environment
        self.currentLevel = levelLoader(environment, level, area)
        self.inventory = []
        self.folder = "./files/environment" + str( environment) 
        self.invotoryAdress = self.folder + "/inventory.dat"

        #initialazation
        self.initInventory()
    #---end init--

    def initInventory(self):
        #inventory initialazation
        contents = None
        try:
            with open(self.invotoryAdress, 'r', encoding='utf-8') as file:
                contents = file.read().split(' ')
            #---end with---
            self.inventory = contents
        except FileNotFoundError as er:
            print("file not found ", er)
        #---end try---
        
        for i in range(len(self.inventory)):
            self.inventory[i] = o.item(self.inventory[i], self.environment)
        #---end for---
    #---end initInventory---

    def nextLevel(self):
        self.currentLevel = levelLoader(self.environment, self.currentLevel.getLevel()+1)
    #---end nextLevel---

    #---Beginning accessor---
    def getInventoryAdress(self):
        return self.invotoryAdress

    def getFolder(self):
        return self.folder

    def getLevel(self):
        return self.currentLevel

    def getInventory(self):
        return self.inventory

    def getItem(self, keyChar):
        for i in self.inventory:
            if (i.getKeyChar() == keyChar):
                return i
            #---end if---
        #---end for---
        return o.item('na', self.environment)

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

    def __init__(self, environment, level, area = 11):
        #setting internal variables
        self.environment = environment
        self.level = level
        self.folder = "./files/environment" + str( environment) + "/level" + str( level)
        self.musicAdress = self.folder + "soundtrack.mp3"
        self.levelStructureAdress = self.folder + "/levelStruct.txt"
        self.levelStructure = []
        self.position = area #11 being the starting board
        self.currentBoard = areaLoader(self.environment, self.level, self.position) 

        #initialazation
        self.initStructure()
    #---end init---

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

    def boardChange(self, direction):
        if (direction == 'n'):
            self.position += 10
        elif (direction == 's'):
            self.position -= 10
        elif (direction == 'o'):
            self.position += 1
        elif (direction == 'e'):
            self.position -= 1
        else:
            self.position += 0 #

        self.currentBoard = areaLoader(self.environment, self.level, self.position)
    #---end boardChange

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
#---end levelLoader---       

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
        self.adress = "./files/environment" + str( environment) + "/level" + str( level)
        self.boardAdress = str(self.adress) + "/board" + str(self.board) + ".dat"
        self.backAdress = str(self.adress) + "/back" + str(self.board) + ".png"
        self.area = []

        #beginning of initialazation 
        self.initBoard()
    #---end init---

    def initBoard(self):
        #board initialazation
        contents = None 

        try:
            with open(self.boardAdress, 'r', encoding='utf-8') as file:
                contents = file.read().split('\n')
            #---end with---

            for i in range(len(contents)):
                contents[i] = strToArray(contents[i])
            #---end for---

            self.area = contents
            
        except FileNotFoundError as er:
            print("file not found ", er)
        #---end try---
    #---end initBoard---


    #---Beginning of accessors---
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
    #---End of accessors---
#---end AreaLoader---

def strToArray(text):
    arrayProduce = []
    for i in text:
        arrayProduce.append(i)
    #---end for---
    return arrayProduce
#--end strToArray---

def fileLoader(folderRoot, file):
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