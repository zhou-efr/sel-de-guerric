"""try:
    with open("C:/Users/gundamzhou/Documents/GitHub/sel-de-guerric/sources/test.txt", "r") as target:
        contents = target.read()
        print(contents)
except FileNotFoundError as identifier:
    print(identifier)"""
import os as os
import pygame 
import loaders as ld

#---backend elements---
testIDE = ld.environmentLoader(1)
tab1 = testIDE.getLevel().getBoard().getArray()

#---pygame elements---
pygame.init()
window = pygame.display.set_mode((150,150))
SIZE_OF_TILES = 50

for i in range(len(tab1)):
    for j in range(len(tab1[i])):
        bufferItem = testIDE.getItem(tab1[i][j])
        window.blit(bufferItem.picture(), (i*SIZE_OF_TILES, j*SIZE_OF_TILES))
    #---end for---
#---end for---

pygame.display.flip()
continuer = 1
while continuer:
	continuer = int(input())

pygame.quit()