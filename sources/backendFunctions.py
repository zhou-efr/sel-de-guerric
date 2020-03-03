"""
author : la tribut des zhou
"""

import objects as o
import math as m
import loaders as l

def hitboxesFileReader(adress):  #Return the list of the objects with their type and their position 
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
                        hu[-1][3] += 1
                        obj[i+k].remove(obj[i+k][j])
                        k += 1
                        j = -1
                    #---end if---
                    j += 1
                #---end for---
            #---end for---
        #---end for---
        
        for ele in hu:  #inversing the vertical coordonate to be more logic in the landmark
            ele[1] = -ele[1]
            ele[3] = -ele[3]
        #---end for---

        return hu
    except (FileNotFoundError, IndexError) as identifier:
        print("error : ", identifier)
        return []
    #---end try---
#---end hitboxesFileReader---

def simpleList(area):
    ent = []
    obj = []
    for e in area.list[:2]:
        ent += e
    #---endfor---
    for e in area.list[2:]:
        obj += e
    #---endfor---
    return ent, obj
#---end simpleList---

def list(adress, environment):
    #lists to fill
    player = []
    entities = []
    walls = []
    exit = []
    #fill the lists
    for i in hitboxesFileReader(adress):
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
#---end list---

def physicLoader(id, distance = 0, speed = 0, dtime = 1, Vmax = 2.5): #give the influence of somthing on the acceleration of an other
    influence = {"x" : 0, "y" : 0}
    if id == "world1":
        influence = {"x" : -speed["x"]*0.05, "y" : -1} #natural decrease of speed and gravity
        #influence = {"x" : 0.3, "y" : -0.5} #debug
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
        influence["x"] = m.log(m.log(n+1)+1) * Vmax
    #---end if---
    return influence
#---end physicLoader---

def acceleration(ent, obj, world):
    #Execute the influence of the world on the entities
    for e in ent:
        worldinfluence = physicLoader("world" + str(world),0,e.speed)
        e.acceleration["x"] += worldinfluence["x"]
        e.acceleration["y"] += worldinfluence["y"]
    #---end for---
    #Move of the player(s)
    inpinfluence = {"x" : 0, "y" : 0}
    if ent[0][0].jump["jump"] == True:
        inpinfluence = physicLoader("player_jump")
    elif ent[0][0].walking["right"] == True:
        inpinfluence = physicLoader("player_right", 0, ent[0][0].speed, ent[0][0].inptime)
    elif ent[0][0].walking["left"] == True:
        inpinfluence = physicLoader("player_left", 0, ent[0][0].speed, ent[0][0].inptime)
    #---end if---
    ent[0][0].acceleration["x"] += inpinfluence["x"]
    ent[0][0].acceleration["y"] += inpinfluence["y"]
    #Check each entities/object and execute their influence on each entities 
    for ele in ent+obj:
        for e in ent:
            distance = ((ele.position["x1"]-e.position["x1"])**2 + (ele.position["y1"]-e.position["y1"])**2)**(1/2)
            if ele in ent:
                speed = ((e.speed["x"])**2 + (e.speed["y"])**2)**(1/2) - ((ele.speed["x"])**2 + (ele.speed["y"])**2)**(1/2)
            else:
                speed = ((e.speed["x"])**2 + (e.speed["y"])**2)**(1/2)
            #---end if---
            influence = physicLoader(ele.keyChar,distance,speed)
            e.acceleration["x"] += influence["x"]
            e.acceleration["y"] += influence["y"]
        #---end for---
    #---end for---
    return ent
#---end acceleration---

def speed(ent):
    #Check each acceleration of the entities
    for e in ent:
        #Add it to the speed
        e.speed["x"] += e.acceleration["x"]
        e.speed["y"] += e.acceleration["y"]
        #Remove the Acceleration
        e.acceleration = {"x" : 0, "y" : 0}
    #---end for---
    return ent
#---end speed---


def hit(ent, obj):
    for n in range(len(ent)):
        e = ent[n]
        hitpoint = {"x" : [], "y" : []}
        dx = e.position["x2"]-e.position["x1"]
        dy = e.position["y2"]-e.position["y1"]

        for ele in obj + ent[:n-1] + ent[n+1:]:
            hitx = True
            if e.speed["x"] + 1 > ele.position["x1"] - e.position["x2"]>0:
                hitposx = {"x" : ele.position["x1"], "y" : e.position["y1"] + (ele.position["x1"] - e.position["x2"])*e.speed["y"]/e.speed["x"], "dist" : 0}
                hitposx["dist"] = ((hitposx["x"] - e.position["x1"])**2 + (hitposx["y"] - e.position["y1"])**2)**(1/2)
            elif e.speed["x"] - 1 < ele.position["x2"] - e.position["x1"]<0:
                hitposx = {"x" : ele.position["x2"], "y" : e.position["y1"] + (ele.position["x2"] - e.position["x1"])*e.speed["y"]/e.speed["x"], "dist" : 0}
                hitposx["dist"] = ((hitposx["x"] - e.position["x1"])**2 + (hitposx["y"] - e.position["y1"])**2)**(1/2)
            else:
                hitx = False
            #---end if---

            hity = True
            if e.speed["y"] - 1 < ele.position["y2"] - e.position["y1"]<0:
                hitposy = {"x" : e.position["x1"] + (ele.position["y2"] + 1 - e.position["y1"])*e.speed["x"]/e.speed["y"], "y" : ele.position["y2"] + 1, "dist" : 0}
                hitposy["dist"] = ((hitposy["x"] - e.position["x1"])**2 + (hitposy["y"] - e.position["y1"])**2)**(1/2)
            elif e.speed["y"] + 1 > ele.position["y1"] - e.position["y2"]>0:
                hitposy = {"x" : e.position["x1"] + (ele.position["y1"] - 1 - e.position["y2"])*e.speed["x"]/e.speed["y"], "y" : ele.position["y1"] - 1, "dist" : 0}
                hitposy["dist"] = ((hitposy["x"] - e.position["x1"])**2 + (hitposy["y"] - e.position["y1"])**2)**(1/2)
            else:
                hity = False
            #---end if---
            if hitx and (ele.position["y1"]>=hitposx["y"]>=ele.position["y2"] or hitposx["y"]>=ele.position["y1"]>=hitposx["y"]+dy):
                hitpoint["x"].append(hitposx)
            #---end if---
            
            if hity and (ele.position["x1"]<=hitposy["x"]<=ele.position["x2"] or hitposy["x"]<=ele.position["x1"]<=hitposy["x"]+dx):
                hitpoint["y"].append(hitposy)
            #---end if---
        #---end for---

        hitpointx = []
        for x in hitpoint["x"]:
            if hitpointx == []:
                hitpointx = [x["x"], x["y"], x["dist"]]
            elif x["dist"] < hitpointx[2]:
                hitpointx = [x["x"], x["y"], x["dist"]]
            #---end if---
        #---end for---

        hitpointy = []
        for y in hitpoint["y"]:
            if hitpointy == []:
                hitpointy = [y["x"], y["y"], y["dist"]]
            elif y["dist"] < hitpointy[2]:
                hitpointy = [y["x"], y["y"], y["dist"]]
            #---end if---
        #---end for---

        e.hit = True
        if hitpointx != [] and (hitpointy == [] or hitpointx[2] > hitpointy[2]):
            e.speed["x"] = 0
            e.position["x1"] = hitpointx[0] - 1
            e.position["x2"] = hitpointx[0] + dx - 1
            e.position["y1"] = hitpointx[1]
            e.position["y2"] = hitpointx[1] + dy
        elif hitpointy != [] and (hitpointx == [] or hitpointx[2] < hitpointy[2]):
            e.speed["y"] = 0
            e.position["x1"] = hitpointy[0]
            e.position["x2"] = hitpointy[0] + dx
            e.position["y1"] = hitpointy[1]
            e.position["y2"] = hitpointy[1] + dy
        elif hitpointx != [] and hitpointy != [] and hitpointx[2] == hitpointy[2]:
            e.speed["x"] = 0
            e.speed["y"] = 0
            e.position["x1"] = hitpointx[0] - 1
            e.position["x2"] = hitpointx[0] + dx - 1
            e.position["y1"] = hitpointy[1]
            e.position["y2"] = hitpointy[1] + dy
            print(hitpointx, hitpointy)
        else:
            e.hit = False
        #---end if---
    #---end for---
#---end hit---



def move(ent, obj):
    hit(ent, obj)
    hit(ent, obj)
    for e in ent:
        e.position["x1"] += e.speed["x"]
        e.position["x2"] += e.speed["x"]
        e.position["y1"] += e.speed["y"] 
        e.position["y2"] += e.speed["y"]
    #---end for---
#---end move---


def worldUpdater(ent, obj, world, inp):
    ent[0][0].updatePlayerInput(inp)
    acceleration(ent, obj, world)
    speed(ent)
    move(ent, obj)
#---end worldUpdater---


def save(id, area, level = 0, environment = 0, newname = ""):
    fileAdress = "./files/environment0/saves/" + str(id) + ".dat"
    try:
        save = open(fileAdress, 'r').read().split('\n')
        save[3] = int(area)
        if level != 0:
            save[2] = int(level)
        #---end if---
        if environment != 0:
            save[1] = int(environment)
        #---end if---
        if newname != "":
            save[0] = newname
        #---end if---
        file = open(fileAdress, 'w')
        s = str(save[0]) + "\n" + str(save[1]) + "\n" + str(save[2]) + "\n" + str(save[3])
        file.write(s)

    except FileNotFoundError:
        print("Wrong save id")
    #---end try---
#---end save---

def loadsave(id):
    fileAdress = "./files/environment0/saves/" + str(id) + ".dat"
    save = open(fileAdress, 'r').read().split('\n')
    return l.environmentLoader(save[1], save[2], save[3])
#---end loadsave---

def stateUpdater(obj):
    for item in obj:
        if item.keyChar == 'm':
            if abs(item.position["x2"] - item.position["x1"]) > abs(item.position["y2"] - item.position["y1"]):
                item.updateState('t')
            elif abs(item.position["x2"] - item.position["x1"]) < abs(item.position["y2"] - item.position["y1"]):
                item.updateState('b')
            #---end if---
        elif item.keyChar == 'c':
            up = False
            down = False
            right = False
            left = False
            for i in obj:
                if i.keyChar == 'm' or i.keyChar == 'c':
                    if i.position["x1"] == item.position["x2"] + 1:
                        right = True
                    elif item.position["x1"] == i.position["x2"] + 1:
                        left = True
                    elif i.position["y2"] == item.position["y1"] + 1:
                        up = True
                    elif item.position["y2"] == i.position["y1"] + 1:
                        down = True
                    #---end if---
                #---end if---
            #---end for---
            if up == True:
                if right == True:
                    item.updateState('[')
                elif left == True:
                    item.updateState(']')
                #---end if---
            elif down == True:
                if right == True:
                    item.updateState('(')
                elif left == True:
                    item.updateState(')')
                #---end if---
            #---end if---
        #---end if---
    #---end for---
#---end stateDetection---