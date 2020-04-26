import time
import pygame
import frontEndFunctions as f
import backendFunctions as b
import objects as o
import loaders as l

#---Initialazation---
#------pygame------
pygame.init()
width = 1366
height = 768
window = pygame.display.set_mode((width, height))
#window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
if height != window.get_rect().bottom:
    height = window.get_rect().bottom
    width = window.get_rect().right
"""resolutions
    for 16*9 tiles
        for 720p
            Tile Size = 80
        for 1080p
            Tile Size = 120 
"""
TILE_SIZE = int(height/9)
icon = pygame.image.load("../files/panda.png")
pygame.display.set_icon(icon)

#------keyboard------
keyMap = {}
try:
    with open("../files/keyboard.dat", 'r') as target:
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
loaded = l.environmentLoader(window, 3, 1)
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

initialShift = 4 if loaded.getEntities()[0].position["x1"]-9 > 0 else loaded.getEntities()[0].position["x1"]

old = [loaded.getEntities()[0].position["x1"]-initialShift,0,loaded.getEntities()[0].position["x1"],loaded.getEntities()[0].position["y1"],loaded.getEntities()[0].position["x1"],loaded.getEntities()[0].position["y1"]]
while lauched:
    lauched = False
    #---Second Loop---
    game = True
    while game and loaded.getEntities()[0].data["state"] != "dead":
        if loaded.levelChanged():
            initialShift = 4 if loaded.getEntities()[0].position["x1"]-9 > 0 else loaded.getEntities()[0].position["x1"]
            old = [loaded.getEntities()[0].position["x1"]-initialShift,0,loaded.getEntities()[0].position["x1"],loaded.getEntities()[0].position["y1"],loaded.getEntities()[0].position["x1"],loaded.getEntities()[0].position["y1"]]
        #---end if---
        old = f.windowUpdate(window, loaded, old, TILE_SIZE)
        inputs = f.inputReader(keyMap, inputs)
        if inputs["pause"][0]:
            game = False
        elif inputs["quit"][0]:
            game = False
            lauched = False
        clock += 1
        time.sleep(0.01)
        pygame.display.flip()
        b.worldUpdater(loaded, inputs)
        #---end if---
    #---end second loop---
    save1 = "..//files//temp//now.png"
    pygame.image.save(window,save1)
    imgo = pygame.image.load(save1).convert()
    angle = 0
    size = 1
    animation = True
    while (height/2)*size > 10 and animation:
        #we get events
        window.fill((0,0,0))
        img = pygame.transform.rotozoom(imgo, angle, size)
        window.blit(img, ((height/2)-((height/2)*size), (width/2)-((width/2)*size)))
        pygame.display.flip()
        time.sleep(0.01)
        for event in pygame.event.get():
            if event.type == pygame.QUIT : #or (event.type == pygame.KEYDOWN and (event.key == pygame.K_ESC or event.key == pygame.K_RETURN)):
                #the boolean take the value False then we quit the loop
                animation = False
                #---end if---
        #---end for---
        angle += 10
        size -= 0.02
    #---end while---
#---end Main loop---

#---end---
print("---end---")
pygame.quit()