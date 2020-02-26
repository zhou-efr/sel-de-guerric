"""
Those Functions are used to load the level physic, and to update it over the time

author : la tribut des zhou
"""

import objects as o

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

def ObjectIddentifier(l):
    obj = []
    ent = []
    #Iddentify if the object is an object or an entitie
    for i in l:
        if i[0] == "p" or i[0] == "e":
            ent.append(i)
        else:
            obj.append(i)
        #---end if---
    #---end for
    return ent, obj
#---end ObjectIddentifier---

def SimpleList(adress):
    return ObjectIddentifier(HitboxesFileReader(adress))
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

def Acceleration(entities, object, world):
    #Check the world's acceleration's property
    #Execute its influence on the entities
    #Check each entities/object 
    #Execute their influences on the entities
    return 0
#---end Acceleration---

def Speed(entities, object):
    #Check each acceleration of the entities
    #Add it to the speed
    #Remove the Acceleration
    return 0
#---end Speed---

def Moove(entities, object):
    #Check the hitboxes of a travel
    #Execute the travel 
    return 0
#---end Moove---
