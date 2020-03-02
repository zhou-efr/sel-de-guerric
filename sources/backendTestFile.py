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
area = l.areaLoader(1, 1, 11)
lists = area.list


8/0 #The error allow to see the variables easly on Visual Code
'''

#Test of the Acceleration and Speed function
'''
area = l.areaLoader(1, 1, 11)
lists = area.list

b.Acceleration(lists[0]+lists[1], lists[2]+lists[3], 1)

#8/0 #The error allow to see the variables easly on Visual Code

b.Speed(lists[0]+lists[1])

8/0 #Same
'''

#Test for Move
'''
area = l.areaLoader(1, 1, 11)
lists = area.list
for i in range(5):
    print(lists[1][0].position)
    b.Acceleration(lists[0]+lists[1], lists[2]+lists[3], 1)
    b.Speed(lists[0]+lists[1])
    b.Move(lists[0]+lists[1], lists[2]+lists[3])
#---end for---

#8/0 #The error allow to see the variables and debug easly on Visual Code
'''

#Test for simple list
'''
area = l.areaLoader(1, 1, 11)
print(area.simpleList)

8/0
'''

#Test save
'''
b.save(1, 11, 2)
env = b.loadsave(1)
'''
