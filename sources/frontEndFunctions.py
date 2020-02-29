"""This file contain all needed function for the user-machine experience

Then we have :
    input functions
        translation input (could be merge with the previous one)
        menu
            first one
            option
            dev one
        programs end (for save state)
    output functions
        print area
        print movement
        animate sprites
        report error (flemme on les laisse se debrouiller seul)    
"""
from copy import deepcopy
import pygame
from pygame.locals import *
import loaders as ld

def printer(testIDE, window, sizeOfTiles, xWorld = 0, yWorld = 0): #WIP
    pygame.init()

    #---backend elements---
    tab1 = testIDE.getLevel().getBoard().getArray()
    windowRect = window.get_rect()
    wallpaper = pygame.transform.scale(pygame.image.load(testIDE.getLevel().getBoard().getBackAdress()).convert(), windowRect.bottomright)
    window.blit(wallpaper, (0,0))
    
    for i in range(len(tab1)):
        for j in range(len(tab1[i])):
            bufferItem = testIDE.getItem(tab1[i][j])
            bufferPicture = pygame.transform.scale(bufferItem.getPicture().convert_alpha(), (sizeOfTiles, sizeOfTiles))
            window.blit(bufferPicture, (j*sizeOfTiles-xWorld, i*sizeOfTiles-yWorld))
        #---end for---
    #---end for---
    
    if (xWorld >= (window.get_width()/2)):
        xWorld = int(window.get_width()/2)

    return xWorld, yWorld
#---end devPrinter---

def windowUpdate(window, environment, sizeOfTiles = -1):
    if (sizeOfTiles <= 0):
        sizeOfTiles = int(window.get_rect().bottom / 9)
    #--end if---

    entities = environment.getEntities()
    
#---end windowUpdate---

def inputReader(inputs):
    rInput = deepcopy(inputs)
    fInput = {}
    for i, j in rInput.items():
        rInput[i] = (False, i)
    #---end for---

    for e in pygame.event.get() :
        if e.type == QUIT:
            rInput[e.type] = (True, e.type)
        elif e.type == KEYDOWN:
            if e.key in inputs.keys():
                rInput[e.key] = (True, e.key)
            else:
                rInput[e.key] = (False, e.key)
            #---end if---
        #---end if---
    #---end for---

    for i, j in inputs.items():
        fInput[j] = rInput[i]
    #---end for---

    return fInput
#---end inputReader---

def inputUpkeep(key):
    for e in pygame.event.get():
        if e.type == KEYUP and e.key == key:
            return False
    return True
#---end inputUpkeep---