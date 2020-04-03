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
from numpy import sign
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

def windowUpdate(window, environment, old, sizeOfTiles = -1):
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
    worldRect = environment.getYcollideRects()
    abscissaPhaseShift = deepcopy(-old[0]) if (worldSize[0]!=windowSize[0]) else 0
    ordinatePhaseShift = 0
    if (len(entities) > 0):
        player = entities[0]

        if(worldSize[0]!=windowSize[0]):
            if (old[0] - old[2] + player.position['x1']) > 0:
                if player.position['x1'] > windowSize[0]*(1/3) and old[0] <= old[0] + player.position["x1"] - old[2]:
                    old[0] = old[0] + player.position["x1"] - old[2] if old[0] + player.position["x1"] - old[2] < worldSize[0]-windowSize[0] else worldSize[0]-windowSize[0]
                if (windowSize[0]*(2/3) > player.position['x1']-old[0] and old[0]>=old[0] + player.position["x1"] - old[2]):
                    old[0] = old[0] + player.position["x1"] - old[2] if old[0] + player.position["x1"] - old[2] < worldSize[0]-windowSize[0] else worldSize[0]-windowSize[0]
                #---end if---
                abscissaPhaseShift = deepcopy(-old[0])
            #---end if---
        #---end if---

        if(worldSize[1]!=windowSize[1]): 
            if player.position["y1"] < (-worldSize[1]+5):
                old[1] = -(worldSize[1] - windowSize[1])
            elif player.position["y1"] > (-5):
                old[1] = 0
            else:
                if (windowSize[1]+old[1]+m.fabs(old[3])-m.fabs(player.position["y1"]) < worldSize[1]-4):
                    old[1] += m.fabs(old[3])-m.fabs(player.position["y1"])
                else:
                    old[1] = -(worldSize[1] - windowSize[1])
                #---end if---
            #---end if---
        #---end if---
        ordinatePhaseShift = deepcopy(old[1])
        old[2] = player.position["x1"]
        old[3] = player.position["y1"]
    #---end if---
    window.blit(environment.getBackground(), (0,0))

    for i in objects:
        for j in range(int(i.position["x2"] - i.position["x1"])+1):
            for k in range(int(m.fabs(i.position["y2"]- i.position["y1"]))+1):
                window.blit(i.getPicture(), ((i.position['x1'] + abscissaPhaseShift + j)*sizeOfTiles, (m.fabs(i.position['y1']) + ordinatePhaseShift + k)*sizeOfTiles))
            #---end for---
        #---end for---
    #---end for---

    for i in entities:
        print(i)
        print((i.position['x1'], m.fabs(i.position['y1'])))
        window.blit(i.getPicture(), ((i.position['x1'] + abscissaPhaseShift)*sizeOfTiles, (m.fabs(i.position['y1']) + ordinatePhaseShift)*sizeOfTiles))
    #---end for---
    return old
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