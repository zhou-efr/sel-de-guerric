import time as t
import pygame
from pygame.locals import *

pygame.init()

w = pygame.display.set_mode((100,100))

c = True

nb_joysticks = pygame.joystick.get_count()
print("Il y a", nb_joysticks, "joystick(s) branché(s)")
if nb_joysticks > 0:
    mon_joystick = pygame.joystick.Joystick(1)
    mon_joystick.init() #Initialisation

    while c:
        for i in pygame.event.get():
            if i.type == QUIT:
                c = False
            if i.type == JOYBUTTONDOWN and i.button == 0:
                print("Boum !")
            if i.type == JOYAXISMOTION and i.value > 0.2:
                print("droite")
            if i.type == JOYAXISMOTION and i.value < -0.2:
                print("gauche")

pygame.quit()