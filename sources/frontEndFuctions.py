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

import pygame
import loaders as ld

def devPrinter(testIDE):
    pygame.init()
    window = pygame.display.set_mode((150,150))
    SIZE_OF_TILES = 50

    #---backend elements---
    tab1 = testIDE.getLevel().getBoard().getArray()

    wallpaper = pygame.image.load(testIDE.getLevel().getBoard().getBackAdress()).convert()
    window.blit(wallpaper, (0,0))
    
    for i in range(len(tab1)):
        for j in range(len(tab1[i])):
            bufferItem = testIDE.getItem(tab1[i][j])
            bufferPicture = pygame.transform.scale(bufferItem.getPicture().convert_alpha(), (SIZE_OF_TILES, SIZE_OF_TILES))
            window.blit(bufferPicture, (j*SIZE_OF_TILES, i*SIZE_OF_TILES))
        #---end for---
    #---end for---

    pygame.display.flip()
    stop = False
    while not stop:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                stop = True
            #---end if---
        #---end for---
    #---end while---

    pygame.quit()
#---end devPrinter---

def devMenu():
    try:
        levelToLoad = input("select the level to load with the following synthax : <environment> <level> \n").split()
    except:
        print("Mais t'es vraiment une sale merde, t'es serieux remplit l'input correctement ptn !")
        return 0
    #---end try---

    levelToLoad = ld.environmentLoader(int(levelToLoad[0]), int(levelToLoad[1]))
    levelAchitecture = levelToLoad.getLevel().getStructure()

    for i in range(len(levelAchitecture)):
        for j in range(len(levelAchitecture[i])):
            print (levelAchitecture[i][j], end = " ")
        #---end for j---
        print("")
    #---end for i---

    try:
        areaToLoad = int(input("enter the code of the area to load : "))
    except:
        print("Mais t'es vraiment une sale merde, t'es serieux remplit l'input correctement ptn !")
        return 0
    levelToLoad.getLevel().setBoard(areaToLoad)
    
    devPrinter(levelToLoad)
    #---end try---
#---end devMenu---

devMenu()
