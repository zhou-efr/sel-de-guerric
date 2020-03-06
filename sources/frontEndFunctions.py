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
import math as m
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
    """"the function which blit everything 
        For more readability I assume that ALL COORDINATES has the form (x,y) as
        y 
        ^
        |
        0,0-->x
        (0,0) being the left top point of the screen
    """
    if (sizeOfTiles <= 0):
        sizeOfTiles = int(window.get_rect().bottom / 9)
    #--end if---

    windowRect = window.get_rect()
    windowSize =(int(windowRect.right/sizeOfTiles),int(windowRect.bottom/sizeOfTiles))
    entities = environment.getEntities()
    objects = environment.getObjects()
    worldSize = (environment.getWidth(),environment.getHeight())
    abscissaPhaseShift = 0
    ordinatePhaseShift = 0
    if (len(entities) > 0):
        player = entities[0]
        phaseShift = lambda x, y: int((x/m.fabs(x))*(m.log(0.6, m.fabs(y))*y))

        if ((worldSize[0] >= windowSize[0]) and (player.position["x1"] >= windowSize[0])):
            abscissaPhaseShift = phaseShift(player.speed['x'], player.vXMax)*sizeOfTiles
        #---end if---

        if ((worldSize[1] >= windowSize[1]) and (player.position["y1"] >= windowSize[1])):
            ordinatePhaseShift = phaseShift(player.speed['y'], player.vYMax)*sizeOfTiles
        #---end if---
    #---end if---
    window.blit(environment.getBackground(), (0,0))

    for i in objects:
        for j in range(int(i.position["x2"] - i.position["x1"])+1):
            for k in range(int(m.fabs(i.position["y2"]- i.position["y1"]))+1):
                window.blit(i.getPicture(), ((i.position['x1'] + abscissaPhaseShift + j)*sizeOfTiles, (m.fabs(i.position['y1']) + ordinatePhaseShift + k)*sizeOfTiles))

    for i in entities:
        window.blit(i.getPicture(), ((i.position['x1'] + abscissaPhaseShift)*sizeOfTiles, (m.fabs(i.position['y1']) + ordinatePhaseShift)*sizeOfTiles))
    #---end for---
#---end windowUpdate---

def inputReader(inputs, odlInputs):
    rInput = deepcopy(inputs)
    fInput = {}
    events = pygame.event.get()
    for i, j in rInput.items():
        rInput[i] = (odlInputs[j][0], i)
    #---end for---
    for e in events:
        if e.type == QUIT:
            rInput[e.type] = (True, e.type)            
        elif e.type == KEYDOWN and e.key in inputs.keys():
            rInput[e.key] = (True, e.key)
        elif e.type == KEYUP and e.key in inputs.keys():
            rInput[e.key] = (False, e.key)
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