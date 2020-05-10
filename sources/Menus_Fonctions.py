import pygame
from pygame.locals import *

    
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
 