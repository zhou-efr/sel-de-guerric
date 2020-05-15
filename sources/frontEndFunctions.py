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
                #---end if---
            #---end for---
        #---end for---
    #---end for---

    for i in entities:
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

def options(window, window_size, keyMap):

    pygame.display.flip()
    fond = pygame.image.load("fond.jpg").convert()
    
    # Colors
    red = pygame.Color(255, 0, 0)
    white = (255, 255, 255)
    blue = (0, 0, 180)
    vert = (22, 207, 100)
    
    pygame.display.flip()

    game = True
    play = True
    while game:
        window.blit(fond, (0,0))
        
        # Return button
        size_return = (window_size[0]*(150/1080), window_size[1]*(75/720))
        button_return = pygame.Surface(size_return)
        x_return = window_size[0]*0.04
        y_return = window_size[1]*0.04
        pos_return = (x_return, y_return)
        pygame.draw.rect(button_return, vert, button_return.get_rect())
        window.blit(button_return, pos_return)
        
        # Command button
        size_command = (window_size[0]*(300/1080), window_size[1]*(100/700))
        button_command = pygame.Surface(size_command)
        x_command = window_size[0]*0.1
        y_command = window_size[1]*0.4 - size_command[1]/2
        pos_command = (x_command, y_command)
        pygame.draw.rect(button_command, vert, button_command.get_rect())
        window.blit(button_command, pos_command)
        
        # Texte retour
        shape_text_return = pygame.font.Font('freesansbold.ttf', 30)
        text_return = shape_text_return.render('Retour', True, blue)
        window.blit(text_return, (x_return - 50 + size_return[0]/2, y_return - 10 + size_return[1]/2))
       
        # Texte Modify command
        shape_text_command = pygame.font.Font('freesansbold.ttf', int(window_size[0]*(30/1080)))
        text_command = shape_text_command.render('Modify Commands', True, blue)
        window.blit(text_command, (x_command + size_command[0]*0.04, y_command + size_command[1]*0.4))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type==VIDEORESIZE:
                window = pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                window_size = event.dict['size']
                pygame.display.flip()
            if event.type == MOUSEBUTTONUP and event.pos[0] > pos_return[0] and event.pos[0] < pos_return[0] + size_return[0]  and event.pos[1] > pos_return[1] and event.pos[1] < pos_return[1] + size_return[1] :
                game = False
            if event.type == MOUSEBUTTONUP and event.pos[0] > x_command and event.pos[0] < x_command + size_command[0] and event.pos[1] > y_command and event.pos[1] < y_command + size_command[1] :
                modify_command(window, window_size, keyMap)
            
        pygame.display.flip()
    
    return game   

   
def rules(window, window_size):
    
    pygame.display.flip()
    
    # Colors
    red = pygame.Color(255, 0, 0)
    white = (255, 255, 255)
    blue = (0, 0, 180)
    vert = (22, 207, 100)
    bleu_clair = (0, 153, 255)
    
    fond = pygame.image.load("fond.jpg").convert()
    
    game = True
    play = True 

    while game:
        
        window.blit(fond, (0,0))
        
        # Return button
        size_return = (window_size[0]*(150/1080), window_size[1]*(75/720))
        button_return = pygame.Surface(size_return)
        x_return = window_size[0]*0.04
        y_return = window_size[1]*0.04
        pos_return = (x_return, y_return)
        pygame.draw.rect(button_return, vert, button_return.get_rect())
        window.blit(button_return, pos_return)
        
        # Texte retour
        shape_text_return = pygame.font.Font('freesansbold.ttf', 30)
        text_return = shape_text_return.render('Retour', True, blue)
        window.blit(text_return, (x_return - 50 + size_return[0]/2, y_return - 10 + size_return[1]/2))
       
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type==VIDEORESIZE:
                window = pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                window_size = event.dict['size']
                pygame.display.flip()
            if event.type == MOUSEBUTTONUP and event.pos[0] > pos_return[0] and event.pos[0] < pos_return[0] + size_return[0]  and event.pos[1] > pos_return[1] and event.pos[1] < pos_return[1] + size_return[1] :
                game = False
                play = True
                       
        pygame.display.flip()


def modify_command(window, window_size, keyMap):
    pygame.display.flip()
    
    # Colors
    red = pygame.Color(255, 0, 0)
    white = (255, 255, 255)
    blue = (0, 0, 180)
    vert = (22, 207, 100)
    bleu_clair = (0, 153, 255)
    
    fond = pygame.image.load("fond.jpg").convert()
    
    game = True
    play = True
    
    while game:
        
        window.blit(fond, (0,0))
        
        # Return button
        size_return = (window_size[0]*(150/1080), window_size[1]*(75/720))
        button_return = pygame.Surface(size_return)
        x_return = window_size[0]*0.04
        y_return = window_size[1]*0.04
        pos_return = (x_return, y_return)
        pygame.draw.rect(button_return, vert, button_return.get_rect())
        window.blit(button_return, pos_return)
        
        # Texte retour
        shape_text_return = pygame.font.Font('freesansbold.ttf', 30)
        text_return = shape_text_return.render('Retour', True, blue)
        window.blit(text_return, (x_return - 50 + size_return[0]/2, y_return - 10 + size_return[1]/2))
        
        ###### Création des boutons pour modifier les touches ######
        
        # z
        size_z = (window_size[0]*(150/1080), window_size[1]*(75/720))
        button_z = pygame.Surface(size_z)
        x_z = window_size[0]*0.3
        y_z = window_size[1]*0.10
        pos_z = (x_z, y_z)
        pygame.draw.rect(button_z, vert, button_z.get_rect())
        window.blit(button_z, pos_z)
        
        shape_text_z = pygame.font.Font('freesansbold.ttf', int(window_size[0]*(30/1080)))
        text_z = shape_text_z.render('UP', True, blue)
        window.blit(text_z, (x_z + size_z[0]*0.3, y_z + size_z[1]*0.2))

        # q
        size_q = (window_size[0]*(150/1080), window_size[1]*(75/720))
        button_q = pygame.Surface(size_q)
        x_q = window_size[0]*0.3
        y_q = window_size[1]*0.25
        pos_q = (x_q, y_q)
        pygame.draw.rect(button_q, vert, button_q.get_rect())
        window.blit(button_q, pos_q)
        
        shape_text_q = pygame.font.Font('freesansbold.ttf', int(window_size[0]*(30/1080)))
        text_q = shape_text_q.render('LEFT', True, blue)
        window.blit(text_q, (x_q + size_q[0]*0.15, y_q + size_q[1]*0.2))
        
        # s
        size_s = (window_size[0]*(150/1080), window_size[1]*(75/720))
        button_s = pygame.Surface(size_s)
        x_s = window_size[0]*0.3
        y_s = window_size[1]*0.40
        pos_s = (x_s, y_s)
        pygame.draw.rect(button_s, vert, button_s.get_rect())
        window.blit(button_s, pos_s)
        
        shape_text_s = pygame.font.Font('freesansbold.ttf', int(window_size[0]*(30/1080)))
        text_s = shape_text_s.render('RIGHT', True, blue)
        window.blit(text_s, (x_s + size_s[0]*0.15, y_s + size_s[1]*0.2))
        
        # d
        size_d = (window_size[0]*(150/1080), window_size[1]*(75/720))
        button_d = pygame.Surface(size_d)
        x_d = window_size[0]*0.3
        y_d = window_size[1]*0.55
        pos_d = (x_d, y_d)
        pygame.draw.rect(button_d, vert, button_d.get_rect())
        window.blit(button_d, pos_d)
        
        shape_text_d = pygame.font.Font('freesansbold.ttf', int(window_size[0]*(30/1080)))
        text_d = shape_text_d.render('DOWN', True, blue)
        window.blit(text_d, (x_d + size_d[0]*0.15, y_d + size_d[1]*0.2))
        
        # jump
        size_jump = (window_size[0]*(150/1080), window_size[1]*(75/720))
        button_jump = pygame.Surface(size_jump)
        x_jump = window_size[0]*0.3
        y_jump = window_size[1]*0.70
        pos_jump = (x_jump, y_jump)
        pygame.draw.rect(button_jump, vert, button_jump.get_rect())
        window.blit(button_jump, pos_jump)
        
        shape_text_jump = pygame.font.Font('freesansbold.ttf', int(window_size[0]*(30/1080)))
        text_jump = shape_text_jump.render('JUMP', True, blue)
        window.blit(text_jump, (x_jump + size_jump[0]*0.15, y_jump + size_jump[1]*0.2))
        
        # bounce
        size_bounce = (window_size[0]*(150/1080), window_size[1]*(75/720))
        button_bounce = pygame.Surface(size_bounce)
        x_bounce = window_size[0]*0.3
        y_bounce = window_size[1]*0.85
        pos_bounce = (x_bounce, y_bounce)
        pygame.draw.rect(button_bounce, vert, button_bounce.get_rect())
        window.blit(button_bounce, pos_bounce)
        
        shape_text_bounce = pygame.font.Font('freesansbold.ttf', int(window_size[0]*(30/1080)))
        text_bounce = shape_text_bounce.render('BOUNCE', True, blue)
        window.blit(text_bounce, (x_bounce + size_bounce[0]*0.15, y_bounce + size_bounce[1]*0.2))
        
        
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type==VIDEORESIZE:
                window = pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                window_size = event.dict['size']
                pygame.display.flip()
            if event.type == MOUSEBUTTONUP and event.pos[0] > pos_return[0] and event.pos[0] < pos_return[0] + size_return[0]  and event.pos[1] > pos_return[1] and event.pos[1] < pos_return[1] + size_return[1] :
                game = options(window, window_size, keyMap)
            if event.type == MOUSEBUTTONUP and event.pos[0] > x_z and event.pos[1] < x_z + size_z[0] and event.pos[1] > y_z and event.pos[1] < y_z + size_z[1] :
                press = True
                while press:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            game = False
                            press = False
                            play = False
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                press = False
                            else :
                                keyMap[event.key] = "up"
                                press = False
                                print(keyMap[event.key])
    
        pygame.display.flip()
        
    return game
 