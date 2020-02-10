import pygame

pygame.init()

def strToArray(text):
    arrayProduce = []
    for i in text:
        arrayProduce.append(i)
    #---end for---
    return arrayProduce
#--end strToArray---

def areaLoader(environment, level, board):
    """area loader .py is the file which containt the loader functions.


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
    #setting internal variables
    environment = environment
    level = level
    board = board
    adress = "C:/Users/gundamzhou/Documents/GitHub/sel-de-guerric/files/environment" + str( environment) + "/level" + str( level) + "/board" + str( board) + ".txt"
    contents = None
    print( adress)
    area = []

    #beginning of initialazation 
    try:
        with open( adress, 'r') as file:
            contents = file.read().split('\n')
        #---end with---

        for i in range(len(contents)):
            contents[i] = strToArray(contents[i])
        #---end for---

        area = contents
        
    except FileNotFoundError:
        print("file not found")
    
    return area
#---end AreaLoader---

def areaPrinter(surface, board, environment):
    print("wip")
#---end areaPrinter---

print(areaLoader(1,1,1))