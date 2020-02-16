import time
import pygame
import frontEndFunctions as f

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
except FileNotFoundError or IndexError as identifier:
    print(identifier, "default qwerty mode will be apply")
    keyMap = {119 : "up",
        115 : "down",
        100 : "right",
        97 : "left",
        305 : "action1",
        32 : "action2",
        27 : "pause",
        12 : "quit"}
#---end try---

#---Main Loop---
lauched = True
while lauched:
    #---Second Loop---
    game = True
    while game:
        inputs = f.inputReader(keyMap)
        if inputs["pause"][0]:
            game = False
        elif inputs["quit"][0]:
            game = False
            lauched = False
        #---end if---
    #---end second loop---
    lauched = False
#---end Main loop---

#---end---
print("---end---")
pygame.quit()