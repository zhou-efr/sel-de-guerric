import time
import pygame
import frontEndFunctions as f
import backendFunctions as b
import objects as o
import loaders as l
from pygame.locals import *
from Menus_Fonctions import *  

#---Initialazation---
#------pygame------
pygame.init()
width = 1366
height = 768
window_size = (width, height)
window = pygame.display.set_mode((width, height), RESIZABLE)
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

keyMap = {119 : "up",
        115 : "down",
        100 : "right",
        97 : "left",
        304 : "action1",
        32 : "action2",
        27 : "pause",
        12 : "quit"}

print(keyMap[119])

TILE_SIZE = int(height/9)
icon = pygame.image.load("../files/panda.png")
pygame.display.set_icon(icon)

red = pygame.Color(255, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 180)
vert = (22, 207, 100)
police = 'Demo.ttf'
fond = pygame.image.load("../sources/fond.jpg").convert()


pygame.display.flip()

play = True

while play:
    pygame.display.flip()
    window.blit(fond, (0,0))
    # Bouton Jouer
    size_jouer = (window_size[0]*(300/1080), window_size[1]*(130/720))
    x = window_size[0]/2 - size_jouer[0]/2
    y = window_size[1]/2 - size_jouer[1]/2 - 90
    pos_rect = (x, y)
        
    rect_filled = pygame.Surface(size_jouer)
    pygame.draw.rect(rect_filled, vert, rect_filled.get_rect())
    window.blit(rect_filled, pos_rect)
        
    # Bouton Options
    size_option = (window_size[0]*(250/1080), window_size[1]*(100/720))
    x_opt = window_size[0]/2 - size_option[0]/2
    y_opt = y + window_size[0]*(100/720)
    option_pos = (x_opt, y_opt)
        
    option_button = pygame.Surface(size_option)
    pygame.draw.rect(option_button, vert, option_button.get_rect())
    window.blit(option_button, option_pos)
        
    # Bouton Rules
    size_rules =  (window_size[0]*(150/1080), window_size[1]*(75/720))
    x_rules = window_size[0]*0.75
    y_rules = window_size[0]*0.08
    rules_pos = (x_rules, y_rules)
        
    rules_button = pygame.Surface(size_rules)
    pygame.draw.rect(rules_button, vert, rules_button.get_rect())
    window.blit(rules_button, rules_pos)
        
    # Texte Jouer
    shape_text = pygame.font.Font(police, 100)
    text_display = shape_text.render('Play', True, blue)
    window.blit(text_display, (x - 90 + size_jouer[0]/2, y - 43 + size_jouer[1]/2))
        
    # Texte Options
    shape_text_opt = pygame.font.Font(police, 40)
    text_option = shape_text_opt.render('Options', True, blue)
    window.blit(text_option, (x_opt - 75 + size_option[0]/2, y_opt - 15 + size_option[1]/2))
       
    # Texte Rules
    shape_text_rules = pygame.font.Font(police, 30)
    text_rules = shape_text_rules.render('RULES', True, blue)
    window.blit(text_rules, (size_rules[0]/2 + window_size[0]*0.75 - 40, size_rules[1]/2 + window_size[0]*0.08 - 12))
        
    for event in pygame.event.get():
        if event.type == QUIT:
            play = False
        if event.type == MOUSEBUTTONUP and event.pos[0] > x_opt and event.pos[0] < x_opt + size_option[0] and event.pos[1] > y_opt and event.pos[1] < y_opt + size_option[1] :
            play = options(window, window_size)
        if event.type==VIDEORESIZE:
            window = pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
            window_size = event.dict['size']
            pygame.display.flip()
        if event.type == MOUSEBUTTONUP and event.pos[0] > x_rules and event.pos[0] < x_rules + size_rules[0] and event.pos[1] > y_rules and event.pos[1] < y_rules + size_rules[1] :
            play = rules(window, window_size)
        if event.type == MOUSEBUTTONUP and event.pos[0] > x and event.pos[0] < x + size_jouer[0] and event.pos[1] > y and event.pos[1] < y + size_jouer[1] :
    #------keyboard------
            print("\nJe passe ici\n")
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
                # def de keyMap ici
            #---end try---

            #------game------
            loaded = l.environmentLoader(window, 1, 1)
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
                    time.sleep(0.0001)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT : #or (event.type == pygame.KEYDOWN and (event.key == pygame.K_ESC or event.key == pygame.K_RETURN)):
                            #the boolean take the value False then we quit the loop
                            animation = False
                            #---end if---
                    #---end for---
                    angle += 10
                    size -= 0.02
                lauched = False
                play = False
    #---end while---
#---end Main loop---

#---end---
print("---end---")
pygame.quit()