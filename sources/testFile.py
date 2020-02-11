"""try:
    with open("C:/Users/gundamzhou/Documents/GitHub/sel-de-guerric/sources/test.txt", "r") as target:
        contents = target.read()
        print(contents)
except FileNotFoundError as identifier:
    print(identifier)"""


import os as os
import pygame 
import loaders as ld


#---pygame elements---
pygame.init()
window = pygame.display.set_mode((150,150))
SIZE_OF_TILES = 50

#---backend elements---
testIDE = ld.environmentLoader(1)
tab1 = testIDE.getLevel().getBoard().getArray()

wallpaper = pygame.image.load(testIDE.getLevel().getBoard().getBackAdress()).convert()
window.blit(wallpaper, (0,0))
print(tab1)
for i in range(len(tab1)):
    for j in range(len(tab1[i])):
        bufferItem = testIDE.getItem(tab1[i][j])
        bufferPicture = pygame.transform.scale(bufferItem.getPicture().convert_alpha(), (SIZE_OF_TILES, SIZE_OF_TILES))
        window.blit(bufferPicture, (j*SIZE_OF_TILES, i*SIZE_OF_TILES))
    #---end for---
#---end for---

pygame.display.flip()
os.system("pause")

print("------board perspective has changed------")
testIDE.getLevel().boardChange('o')
tab1 = testIDE.getLevel().getBoard().getArray()

wallpaper = pygame.image.load(testIDE.getLevel().getBoard().getBackAdress()).convert()
window.blit(wallpaper, (0,0))
print(tab1)
for i in range(len(tab1)):
    for j in range(len(tab1[i])):
        print(tab1[i][j])
        bufferItem = testIDE.getItem(tab1[i][j])
        bufferPicture = pygame.transform.scale(bufferItem.getPicture().convert_alpha(), (SIZE_OF_TILES, SIZE_OF_TILES))
        window.blit(bufferPicture, (j*SIZE_OF_TILES, i*SIZE_OF_TILES))
    #---end for---
#---end for---

pygame.display.flip()
os.system("pause")


pygame.quit()
