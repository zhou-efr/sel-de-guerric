import backendFunctions as b
import loaders as l

'''
This is backend Test File to see the input and out put, and the different interaction between backend's functions

author : la tribut des zhou
'''

#Test of the HitboxesFileReader
'''
adress = "./files/environment1/level1/boxes11.dat"
print(b.HitboxesFileReader(adress))
'''

#Test of lists
'''
level = l.levelLoader(1, 1)  #make the line of self.picture off and also the lines of the updateSprite method
lists = level.list


8/0 #The error allow to see the variables easly on Visual Code
'''

#Test of the Acceleration and Speed function
'''
level = l.levelLoader(1, 1)  #make the line of self.picture off and also the lines of the updateSprite method
lists = level.list

b.Acceleration(lists[0]+lists[1], lists[2]+lists[3], 1)

#8/0 #The error allow to see the variables easly on Visual Code

b.Speed(lists[0]+lists[1])

8/0 #Same
'''

#Test for Move

level = l.levelLoader(1, 1)  #make the line of self.picture off and also the lines of the updateSprite method
lists = level.list
for i in range(5):
    print(lists[1][0].position)
    b.Acceleration(lists[0]+lists[1], lists[2]+lists[3], 1)
    b.Speed(lists[0]+lists[1])
    b.Move(lists[0]+lists[1], lists[2]+lists[3])
#---end for---

#8/0 #The error allow to see the variables and debug easly on Visual Code
