import time as t
import pygame

pygame.init()

w = pygame.display.set_mode((500, 500))
imgo = pygame.image.load("pandauwu.png")
angle = 0
size = 1
animation = True
while animation:
    #we get events
    w.fill((0,0,0))
    img = pygame.transform.rotozoom(imgo, angle, size)
    w.blit(img, (250-(61*size), 250-(61*size)))
    pygame.display.flip()
    t.sleep(0.1)
    angle += 10
    size -= 0.01
#---end while---

pygame.quit()
#---end---