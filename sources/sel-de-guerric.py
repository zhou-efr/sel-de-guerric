import time
import pygame
import frontEndFunctions as f
import backendFunctions as b
import objects as o
import loaders as l

#---Initialazation---
#------pygame------
pygame.init()
width = 1280
height = 720
window = pygame.display.set_mode((width, height))
"""resolutions
    for 16*9 tiles
        for 720p
            Tile Size = 80
        for 1080p
            Tile Size = 120 
"""
TILE_SIZE = int(height/9)

#------keyboard------
keyMap = {}
try:
    with open("./files/keyboard.dat", 'r') as target:
        contents = target.read().split("\n")
    #---end with---

    for i in range(len(contents)):
        contents[i] = contents[i].split()
        contents[i][1] = int(contents[i][1])
        keyMap[contents[i][1]] = contents[i][0]
    #---end for---
except (FileNotFoundError, IndexError) as identifier:
    print(identifier, "default qwerty mode will be apply")
    keyMap = {119 : "up",
        115 : "down",
        100 : "right",
        97 : "left",
        304 : "action1",
        32 : "action2",
        27 : "pause",
        12 : "quit"}
#---end try---

#------game------
loaded = l.environmentLoader(window, 1, 1, 11)
clock = 0 #in ms
inputs = {"up" : (False, 0),
        "down" : (False, 0),
        "right" : (False, 0),
        "left" : (False, 0),
        "action1" : (False, 0),
        "action2" : (False, 0),
        "pause" : (False, 0),
        "quit" : (False, 0)}
#---Main Loop---
lauched = True

old = [loaded.getEntities()[0].position["x1"],0,loaded.getEntities()[0].position["x1"],loaded.getEntities()[0].position["y1"],loaded.getEntities()[0].position["x1"],loaded.getEntities()[0].position["y1"]]
while lauched:
    lauched = False
    #---Second Loop---
    game = True
    while game:
        if loaded.isChanged():
            old = [loaded.getEntities()[0].position["x1"],0,loaded.getEntities()[0].position["x1"],loaded.getEntities()[0].position["y1"],loaded.getEntities()[0].position["x1"],loaded.getEntities()[0].position["y1"]]
        #---end if---
        old = f.windowUpdate(window, loaded, old, TILE_SIZE)
        inputs = f.inputReader(keyMap, inputs)
        if inputs["pause"][0]:
            game = False
        elif inputs["quit"][0]:
            game = False
            lauched = False
        clock += 1
        time.sleep(0.05)
        pygame.display.flip()
        b.worldUpdater(loaded, inputs)
        #---end if---
    #---end second loop---
#---end Main loop---

#---end---
print("---end---")
pygame.quit()