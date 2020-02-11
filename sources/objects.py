"""object.py
    this file contain all objects needed
    for instance:
        items

author : la tribut des zhou
"""
import pygame

pygame.init()

class item:
    """item, the main class, all others object are inherent to this one
        Work In Progress (wip)
        j'ai fait ce dont j'avais besoin je vous laisserai probablement le reste vue que c'est du backend
        C'est pas par ce que je l'ai cree que vous avez a la garder
    """
    def __init__(self, keyChar, environment):
        self.keyChar = keyChar
        self.pictureAdress = "../files/environment" + str( environment) + "/" + keyChar + ".png"
        self.picture = pygame.image.load(self.pictureAdress)
    #---end init---

    #---beginning accessors
    def getKeyChar(self):
        return self.keyChar
    
    def getPictureAdress(self):
        return self.pictureAdress
    
    def getPicture(self):
        return self.picture
    #---end accessors---
