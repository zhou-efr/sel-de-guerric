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
        for i in range(l):
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
            player.append(o.player())
            player[-1].position["y1"] = i[1]
            player[-1].position["y2"] = i[3]
            player[-1].position["x1"] = i[2]
            player[-1].position["x2"] = i[4]
        elif i[0] == "e":
            entities.append(o.entities("e", environment))
            entities[-1].position["y1"] = i[1]
            entities[-1].position["y2"] = i[3]
            entities[-1].position["x1"] = i[2]
            entities[-1].position["x2"] = i[4]
        elif i[0] == "s":
            exit.append(o.item("s", environment))
            exit[-1].position["y1"] = i[1]
            exit[-1].position["y2"] = i[3]
            exit[-1].position["x1"] = i[2]
            exit[-1].position["x2"] = i[4]
        else:
            walls.append(o.item(i[0], environment))
            walls[-1].position["y1"] = i[1]
            walls[-1].position["y2"] = i[3]
            walls[-1].position["x1"] = i[2]
            walls[-1].position["x2"] = i[4]
        #---end if---
    #---end for---
    return player, entities, exit, walls
#---end List---

def physicLoader(id,distance,dtime,speed): #give the influence of somthing on the acceleration of an other
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
        worldinfluence = physicLoader("world" + str(world),0,0,((e.speed["x"])**2 + (e.speed["y"])**2)**(1/2))
        e.acceleration["x"] += worldinfluence["x"]
        e.acceleration["y"] += worldinfluence["y"]
    #---end for---
    #Check each entities/object and execute their influence on each entities 
    for ele in ent+obj:
        for e in ent:
            distance = ((ele.position["x1"]-e.position["x1"])**2 + (ele.position["y1"]-e.position["y1"])**2)**(1/2)
            if ele in ent:
                speed = ((e.speed["x"])**2 + (e.speed["y"])**2)**(1/2) - ((ele.speed["x"])**2 + (ele.speed["y"])**2)**(1/2)
            else:
                speed = ((e.speed["x"])**2 + (e.speed["y"])**2)**(1/2)
            #---end if---
            influence = physicLoader(ele.keyChar,distance,0,speed)
            e.acceleration["x"] += influence["x"]
            e.acceleration["y"] += influence["y"]
        #---end for---
    #---end for---
    return ent
#---end Acceleration---

def Speed(ent):
    #Check each acceleration of the entities
    for e in ent:
        #Add it to the speed
        e.speed["x"] += e.acceleration["x"]
        e.speed["y"] += e.acceleration["y"]
        #Remove the Acceleration
        e.acceleration = {"x" : 0, "y" : 0}
    #---end for---
    return ent
#---end Speed---

def HorizontalHit(ent, obj):
    for e in ent:
        hitpoint = []
        coef = e.speed["y"]/e.speed["x"]
        dx = e.position["x2"]-e.position["x1"] #size x of the entitie
        for hit in obj+ent:
            col = True
            if e.speed["x"] <= hit.position["x2"]-e.position["x1"]: 
                ens = {"y1" : e.position["y1"] + coef*(hit.position["x2"]-e.position["x1"]), "y2" : e.position["y1"] + coef*(hit.position["x2"]-e.position["x1"]), "x" : hit.position["x2"]}
                i = 0
            elif e.speed["x"] >= hit.position["x1"]-e.position["x2"]:
                ens = {"y1" : e.position["y1"] + coef*(hit.position["x1"]-e.position["x2"]), "y2":e.position["y1"] + coef*(hit.position["x1"]-e.position["x2"]), "x" : hit.position["x1"]}
                i = 1
            else:
                col = False
            #---end if---
            if col and (ens["y1"] < hit.position["y1"] < ens["y2"] or hit.position["y1"] < ens["y1"] < hit.position["y2"]):
                hitpoint.append([i,ens])
            #---end if---
        #---end for---
        hit = []
        for h in hitpoint:
            if hit == []:
                hit = h
            elif ((h[1]["y1"]**2 + h[1]["y2"]**2)**(1/2) < (hit[1]["y1"]**2 + hit[1]["y2"]**2)**(1/2)):
                hit = h
            #---end if---
        #---end for---

        if hit != []:
            if hit[0] == 0:
                e.speed["x"] = 0
                e.speed["y"] -= hit[1]["y1"] - e.position["y1"]
                e.position["x1"] = hit[1]["x"]
                e.position["x2"] = hit[1]["x"] + dx
                e.position["y1"] = hit[1]["y1"]
                e.position["y2"] = hit[1]["y2"]
            else:
                e.speed["x"] = 0
                e.speed["y"] -= hit[1]["y1"] - e.position["y1"]
                e.position["x1"] = hit[1]["x"] - dx
                e.position["x2"] = hit[1]["x"]
                e.position["y1"] = hit[1]["y1"]
                e.position["y2"] = hit[1]["y2"]
            #---end if---
        #---end if---
    #---end for---

    return ent
#---end HorizontalHit---

def VerticalHit(ent, obj):
    for e in ent:
        hitpoint = []
        coef = e.speed["x"]/e.speed["y"]
        dy = e.position["y2"]-e.position["y1"] #size y of the entitie
        for hit in obj+ent:
            col = True
            if e.speed["y"] <= hit.position["y2"]-e.position["y1"]: 
                ens = {"x1" : e.position["x1"] + coef*(hit.position["y2"]-e.position["y1"]), "x2" : e.position["x1"] + coef*(hit.position["y2"]-e.position["y1"]), "y" : hit.position["y2"]}
                i = 0
            elif e.speed["y"] >= hit.position["y1"]-e.position["y2"]:
                ens = {"x1" : e.position["x1"] + coef*(hit.position["y1"]-e.position["y2"]), "x2":e.position["x1"] + coef*(hit.position["y1"]-e.position["y2"]), "y" : hit.position["y1"]}
                i = 1
            else:
                col = False
            #---end if---
            if col and (ens["x1"] < hit.position["x1"] < ens["x2"] or hit.position["x1"] < ens["x1"] < hit.position["x2"]):
                hitpoint.append([i,ens])
            #---end if---
        #---end for---
        hit = []
        for h in hitpoint:
            if hit == []:
                hit = h
            elif ((h[1]["x1"]**2 + h[1]["x2"]**2)**(1/2) < (hit[1]["x1"]**2 + hit[1]["x2"]**2)**(1/2)):
                hit = h
            #---end if---
        #---end for---

        if hit != []:
            if hit[0] == 0:
                e.speed["y"] = 0
                e.speed["x"] -= hit[1]["x1"] - e.position["x1"]
                e.position["y1"] = hit[1]["y"]
                e.position["y2"] = hit[1]["y"] + dy
                e.position["x1"] = hit[1]["x1"]
                e.position["x2"] = hit[1]["x2"]
            else:
                e.speed["y"] = 0
                e.speed["x"] -= hit[1]["x1"] - e.position["x1"]
                e.position["y1"] = hit[1]["y"] - dy
                e.position["y2"] = hit[1]["y"]
                e.position["x1"] = hit[1]["x1"]
                e.position["x2"] = hit[1]["x2"]
            #---end if---
        #---end if---
    #---end for---

    return ent
#---end VerticalHit---

def Move(ent, obj):
    HorizontalHit(ent, obj)
    VerticalHit(ent, obj)
    for e in ent:
        e.position["x"] += e.speed["x"]
        e.position["y"] += e.speed["y"]
    #---end for---
#---end move---