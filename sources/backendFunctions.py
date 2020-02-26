"""
Those Functions are used to load the level physic, and to update it over the time

author : la tribut des zhou
"""

import objects as o
import math as m

def HitboxesFileReader(adress):  #Return the list of the objects with their type and their position 
    #Load the fill
    try:
        with open(adress, 'r') as target:
            contents = target.read().split("\n")
        #---end with---

        #Read it character by character
        obj = []
        l = 0
        for line in contents:
            c = 0
            nospace = True
            obj.append([])
            for char in line:
                if char != " ":
                    if c > 0 and char == obj[l][-1][0] and nospace == True:
                        #Compact line object
                        obj[l][-1][4] += 1
                    else:
                        #Add the new object tiles with his type, and his position
                        obj[l].append([char,l,c,l,c])
                        nospace = True
                    #---end if---
                else:
                    nospace = False
                #---end if---
                c += 1
            #---end for---
            l += 1
        #---end for---
            
        #Compact column object
        hu=[]
        for i in range(l-1):
            for o in obj[i]:
                hu.append(o)
                j = 0
                k = 1
                while i+k < l and j < len(obj[i+k]):
                    if o[2] == obj[i+k][j][2] and o[4] == obj[i+k][j][4] and o[0] == obj[i+k][j][0]:
                        print(o, obj[i+k][j])
                        hu[-1][3] += 1
                        obj[i+k].remove(obj[i+k][j])
                        k += 1
                        j = -1
                    #---end if---
                    j += 1
                #---end for---
            #---end for---
        #---end for---
            
        return hu
    except (FileNotFoundError, IndexError) as identifier:
        print("error : ", identifier)
        return []
    #---end try---
#---end HitboxesFileReader---

def SimpleList(adress, environment):
    ent = []
    obj = []
    for e in List(adress, environment)[:1]:
        ent += e
    #---endfor---
    for e in List(adress, environment)[2:]:
        obj += e
    #---endfor---
    return ent, obj
#---end SimpleList---

def List(adress, environment):
    #lists to fill
    player = []
    entities = []
    walls = []
    exit = []
    #fill the lists
    for i in HitboxesFileReader(adress):
        if i[0] == "p":
            player.append(o.player("p", environment))
            player[-1].position["x1"] = i[1]
            player[-1].position["x2"] = i[3]
            player[-1].position["y1"] = i[2]
            player[-1].position["y2"] = i[4]
        elif i[0] == "e":
            entities.append(o.entities("e", environment))
            entities[-1].position["x1"] = i[1]
            entities[-1].position["x2"] = i[3]
            entities[-1].position["y1"] = i[2]
            entities[-1].position["y2"] = i[4]
        elif i[0] == "s":
            exit.append(o.item("s", environment))
            exit[-1].position["x1"] = i[1]
            exit[-1].position["x2"] = i[3]
            exit[-1].position["y1"] = i[2]
            exit[-1].position["y2"] = i[4]
        else:
            walls.append(o.item(i[0], environment))
            walls[-1].position["x1"] = i[1]
            walls[-1].position["x2"] = i[3]
            walls[-1].position["y1"] = i[2]
            walls[-1].position["y2"] = i[4]
        #---end if---
    #---end for---
    return player, entities, exit, walls
#---end List---

def physicLoader(id,distance,dtime,speed): #give the influence of sopthing on the acceleration of an other
    influence = {"x" : 0, "y" : 0}
    if id == "world1":
        influence = {"x" : -speed*0.05, "y" : -1} #natural decrease of speed and gravity
    elif id == "player_jump":
        influence["y"] = 5
    elif id == "player_right":
        if dtime <= 1:
            n = abs(-dtime^3+2*dtime)
        else:
            n = abs(1/dtime)
        #---endif---
        influence["x"] = -m.log(m.log(n+1)+1)
    elif id == "player_left":
        if dtime <= 1:
            n = abs(-dtime^3+2*dtime)
        else:
            n = abs(1/dtime)
        #---endif---
        influence["x"] = m.log(m.log(n+1)+1)
    #---end if---
    return influence
#---end physicLoader---

def Acceleration(ent, obj, world):
    #Execute the influence of the world on the entities
    for e in ent:
        worldinfluence = physicLoader("world" + str(world),0,0,e.speed)
        e.acceleration += worldinfluence
    #---end for---
    #Check each entities/object and execute their influence on each entities 
    for ele in ent+obj:
        for e in ent:
            distance = ((ele.position["x1"]-e.position["x1"])**2 + (ele.position["y1"]-e.position["y1"])**2)**(1/2)
            speed = e.speed - ele.speed
            influence = physicLoader(ele.keychar,distance,0,speed)
            e.acceleration += influence
        #---end for---
    #---end for---
    return ent
#---end Acceleration---

def Speed(ent):
    #Check each acceleration of the entities
    for e in ent:
        #Add it to the speed
        e.speed += e.acceleration
        #Remove the Acceleration
        e.acceleration = 0
    #---end for---
    return ent
#---end Speed---

def Moove(entities, object):
    #Check the hitboxes of a travel
    #Execute the travel 
    return 0
#---end Moove---
