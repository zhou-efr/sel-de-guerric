"""
author : la tribut des zhou
"""

import objects as o
import math as m
import loaders as l
import random as r

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
                    if c == 0 or (len(obj[l]) > 0 and char != obj[l][-1][0]) or nospace == False or char == "c":
                        #Add the new object tiles with his type, and his position
                        obj[l].append([char,l,c,l,c])
                        nospace = True
                    else:
                        #Compact line object
                        obj[l][-1][4] += 1
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
                    if o[2] == obj[i+k][j][2] and o[4] == obj[i+k][j][4] and o[0] == obj[i+k][j][0] and o[0] != 'c':
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
    zone = {"ent": [], "obj": []}
    for e in area.list[:3]:
        ent += e
    #---endfor---
    for e in area.list[3:4]:
        obj += e
    #---endfor---
    for e in area.list[4:5]:
        zone["ent"] += e
    #---end for---
    for e in area.list[5:]:
        zone["obj"] += e
    #---end for---
    return ent, obj, zone
#---end simpleList---

def list(board):
    #lists to fill
    player = []
    fish = []
    rat = []
    fspot = []
    walls = []
    cloud = []
    exit = []
    zrat = []
    #fill the lists
    for i in hitboxesFileReader(board.boardAdress):
        if i[0] == "p":
            player.append(o.player())
            player[-1].position["y1"] = i[1]
            player[-1].position["y2"] = i[3]
            player[-1].position["x1"] = i[2]
            player[-1].position["x2"] = i[4]
        elif i[0] == "f":
            fish.append(o.fish(i[0], board))
            fish[-1].position["y1"] = i[1]
            fish[-1].position["y2"] = i[3]
            fish[-1].position["x1"] = i[2]
            fish[-1].position["x2"] = i[4]
        elif i[0] == "r":
            rat.append(o.entities(i[0], board.environment))
            rat[-1].position["y1"] = i[1]
            rat[-1].position["y2"] = i[3]
            rat[-1].position["x1"] = i[2]
            rat[-1].position["x2"] = i[4]
        elif i[0] == "m" or i[0] == "c":
            walls.append(o.item(i[0], board.environment))
            walls[-1].position["y1"] = i[1]
            walls[-1].position["y2"] = i[3]
            walls[-1].position["x1"] = i[2]
            walls[-1].position["x2"] = i[4]
        #---end if---
    #---end for---
    for i in board.boardata["zone"]:
        for j in board.boardata[i]:
            if i == "nt":
                cloud.append(o.entities("nt", board.environment))
                cloud[-1].position["y1"] = j["y1"]
                cloud[-1].position["y2"] = j["y2"]
                cloud[-1].position["x1"] = j["x1"]
                cloud[-1].position["x2"] = j["x2"]
            elif i == "ex":
                exit.append(o.item("ex", board.environment))
                exit[-1].position["y1"] = j["y1"]
                exit[-1].position["y2"] = j["y2"]
                exit[-1].position["x1"] = j["x1"]
                exit[-1].position["x2"] = j["x2"]
            elif i == "s":
                fspot.append(o.item(i, board.environment))
                fspot[-1].position["y1"] = j["y1"]
                fspot[-1].position["y2"] = j["y2"]
                fspot[-1].position["x1"] = j["x1"]
                fspot[-1].position["x2"] = j["x2"]
            elif i == "zrat":
                zrat.append(o.item("zrat", board.environment))
                zrat[-1].position["y1"] = j["y1"]
                zrat[-1].position["y2"] = j["y2"]
                zrat[-1].position["x1"] = j["x1"]
                zrat[-1].position["x2"] = j["x2"]
            #---end if---
        #---end for---
    #---end for---
    return player, fish, rat, walls, cloud, exit, fspot, zrat
#---end list---

def physicLoader(id, ele = None, distance = 0, speed = 0, dtime = 1, Vmax = 0.5): #give the influence of somthing on the acceleration of an other
    influence = {"x" : 0, "y" : 0}
    if id == "world1":
        influence = {"x" : 0, "y" : -0.05} #natural decrease of speed and gravity
    elif id == "player_jump":
        influence["y"] = (1/dtime - 1/10)*0.4
    elif id == "player_double_jump":
        influence["y"] = -speed["y"] + 0.6
    elif id == "player_wall_jump":
        influence["y"] = 0.75
        if ele == 0:
            influence["x"] = 0.4
        else:
            influence["x"] = -0.4
        #---end if---
    elif id == "player_fastfall":
        influence["y"] = -0.85
    elif id == "player_right":
        if speed["x"]<0:
            influence["x"] = -speed["x"]
        elif speed["x"]<Vmax:
            d = 1/(1-speed["x"]/Vmax)+1
            influence["x"] = 1/(1+d)**2
        #---end if---
    elif id == "player_left":
        if speed["x"]>0:
            influence["x"] = -speed["x"]
        elif speed["x"]>-Vmax:
            d = 1/(1+speed["x"]/Vmax)+1
            influence["x"] = -1/(1+d)**2
        #---end if---
    elif id == "stopx":
        influence["x"] = -speed["x"]*0.8
    elif id == "wall":
        influence["y"] = -speed["y"]*0.4
    elif id == "nt" and (type(ele[0]) == type(ele[1]) or type(ele[0]) == o.player):
        if speed != 0 and (ele[0].position["x1"] - ele[1].speed["x"] <= ele[1].position["x1"] <= ele[0].position["x2"] + ele[1].speed["x"] or ele[1].position["x1"] - ele[0].speed["x"] <= ele[0].position["x1"] <= ele[1].position["x2"] + ele[0].speed["x"]) and (ele[0].position["y1"] - ele[1].speed["y"] <= ele[1].position["y1"] <= ele[0].position["y2"] + ele[1].speed["y"] or ele[1].position["y1"] - ele[0].speed["y"] <= ele[0].position["y1"] <= ele[1].position["y2"] + ele[0].speed["y"]):
            influence["x"] += 0.2 * (ele[0].speed["x"]**2 + ele[1].speed["x"]**2)**(1/2)
            influence["y"] += 0.2 * (ele[0].speed["y"]**2 + ele[1].speed["y"]**2)**(1/2)
        elif ele[0] == ele[1]:
            if ele[1].inptime >= 113 or ele[1].inptime < 88:
                ele[1].inptime = 88
            #---end if---
            influence["y"] += m.cos(ele[1].inptime/4) + 1
            ele[1].inptime += 1
        #---end if---
    elif id == "f":
        if ele[0] == ele[1]:
            if ele[1].state == "jump" and ele[1].hit["floor"]:
                if ele[1].data["state"] == "go_right" or ele[1].data["newState"] == "go_right":
                    target = ele[1].r_spot
                else:
                    target = ele[1].l_spot
                #---end if---
                distance = ((target.position["x1"] - ele[1].position["x1"])**2 + (target.position["y1"] - ele[1].position["y1"])**2)**(1/2)
                influence["x"] += (target.position["x1"] - ele[1].position["x1"])/(2 *distance) - ele[1].acceleration["x"]*distance
                influence["y"] += (target.position["y1"] - ele[1].position["y1"])/(2 *distance) - ele[1].acceleration["y"]*distance
            elif ele[1].state == "ground" and ele[1].hit["floor"]:
                if ele[1].data["state"] == "ground_left":
                    influence["x"] = -0.1 - ele[1].speed["x"]
                elif ele[1].data["state"] == "ground_right":
                    influence["x"] = 0.1 - ele[1].speed["x"]
                #---end if---
            elif ele[1].hit["floor"]:
                influence["x"] = -ele[1].speed["x"]*0.8
            #---end if---
        elif ele[1].state == "attack" and type(ele[0]) == o.player and ele[1].hit["floor"]:
            influence["x"] += (ele[0].position["x1"] - ele[1].position["x1"])/(2*distance) - ele[1].acceleration["x"]*distance
            influence["y"] += (ele[0].position["y1"] - ele[1].position["y1"])/(2*distance) - ele[1].acceleration["y"]*distance
        #---end if---
    #---end if---
    return influence
#---end physicLoader---

def acceleration(ent, obj, world):
    #Execute the influence of the world on the entities
    for e in ent:
        worldinfluence = physicLoader("world" + str(world), None, None,e.speed)
        e.acceleration["x"] += worldinfluence["x"]
        e.acceleration["y"] += worldinfluence["y"]
    #---end for---
    #Move of the player(s)
    inp = False
    inpinfluence = {"x" : -0.2 * ent[0].speed["x"], "y" : 0}
    if ent[0].hit["floor"]:
        ent[0].cdw = {"walljump": True, "jump": True, "double_jump": False, "action": ent[0].cdw["action"]}
    if ent[0].hit["rwall"] or ent[0].hit["lwall"]:
        influence = physicLoader("wall", None, None, ent[0].speed)
        inpinfluence["y"] += influence["y"]
    
    if ent[0].jump["jump"]:
        inp = True
        if ent[0].cdw["jump"]:
            influence = physicLoader("player_jump", None, None, None, ent[0].inptime)
            inpinfluence["x"] += influence["x"]
            inpinfluence["y"] += influence["y"]
        if ent[0].cdw["double_jump"]:
            influence = physicLoader("player_double_jump", None, None, ent[0].speed, ent[0].inptime)
            inpinfluence["x"] += influence["x"]
            inpinfluence["y"] += influence["y"]
            ent[0].cdw["double_jump"] = False
        if ent[0].hit["lwall"] and ent[0].cdw["walljump"]:
            influence = physicLoader("player_wall_jump", 0)
            inpinfluence["x"] += influence["x"]
            inpinfluence["y"] += influence["y"]
            ent[0].cdw["walljump"] = False
        if ent[0].hit["rwall"] and ent[0].cdw["walljump"]:
            influence = physicLoader("player_wall_jump", 1)
            inpinfluence["x"] += influence["x"]
            inpinfluence["y"] += influence["y"]
            ent[0].cdw["walljump"] = False
        #---end ifs---
    elif ent[0].cdw["jump"]:
        ent[0].cdw["jump"] = False
        ent[0].inpinfluence = 1
    
    if ent[0].jump["fastfall"]:
        influence = physicLoader("player_fastfall")
        inpinfluence["y"] += influence["y"]
    if ent[0].walking["right"] == True:
        inp = True
        influence = physicLoader("player_right", None, None, ent[0].speed, ent[0].inptime)
        inpinfluence["x"] += influence["x"]
        inpinfluence["y"] += influence["y"]
    if ent[0].walking["left"] == True:
        inp = True
        influence = physicLoader("player_left", None, None, ent[0].speed, ent[0].inptime)
        inpinfluence["x"] += influence["x"]
        inpinfluence["y"] += influence["y"]
    if ent[0].hit["floor"] and not(inp):
        inpinfluence = physicLoader("stopx", None, None, ent[0].speed)
    #---end ifs---
    ent[0].acceleration["x"] += inpinfluence["x"]
    ent[0].acceleration["y"] += inpinfluence["y"]
    #Check each entities/object and execute the influence of each item on it 
    for e in ent:
        for ele in ent+obj:
            distance = ((ele.position["x1"]-e.position["x1"])**2 + (ele.position["y1"]-e.position["y1"])**2)**(1/2)
            if ele in ent:
                speed = ((e.speed["x"])**2 + (e.speed["y"])**2)**(1/2) - ((ele.speed["x"])**2 + (ele.speed["y"])**2)**(1/2)
            else:
                speed = e.speed
            #---end if---
            influence = physicLoader(e.keyChar,[ele,e],distance,speed)
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

def hit(en, obj, zone):
    for n in range(len(en) + len(zone["ent"])):
        if n<len(en):
            e = en[n]
            ent = en[:n] + en[n+1:]
        else:
            e = zone["ent"][n-len(en)]
            ent = []
        #---end if---
        hitpoint = {"x" : [], "y" : []}
        dx = e.position["x2"]-e.position["x1"]
        dy = e.position["y2"]-e.position["y1"]

        for ele in obj + ent:
            hitx = True
            if e.speed["x"] > ele.position["x1"] - e.position["x2"] - 1 >= 0:
                hitposx = {"x" : ele.position["x1"] - 1 - dx, "y" : e.position["y1"] + (ele.position["x1"] - e.position["x2"] - 1)*e.speed["y"]/e.speed["x"], "dist" : 0, "id": "r"}
                hitposx["dist"] = ((hitposx["x"] - e.position["x1"])**2 + (hitposx["y"] - e.position["y1"])**2)**(1/2)
            elif e.speed["x"] < ele.position["x2"] + 1 - e.position["x1"] <= 0:
                hitposx = {"x" : ele.position["x2"] + 1, "y" : e.position["y1"] + (ele.position["x2"] + 1 - e.position["x1"])*e.speed["y"]/e.speed["x"], "dist" : 0, "id": "l"}
                hitposx["dist"] = ((hitposx["x"] - e.position["x1"])**2 + (hitposx["y"] - e.position["y1"])**2)**(1/2)
            else:
                hitx = False
            #---end if---

            hity = True
            if e.speed["y"] < ele.position["y1"] - e.position["y2"] + 1 <= 0:
                hitposy = {"x" : e.position["x1"] + (ele.position["y2"] + 1 - e.position["y1"])*e.speed["x"]/e.speed["y"], "y" : ele.position["y2"] + 1 - dy, "dist" : 0, "id": "floor"}
                hitposy["dist"] = ((hitposy["x"] - e.position["x1"])**2 + (hitposy["y"] - e.position["y1"])**2)**(1/2)
            elif e.speed["y"] > ele.position["y2"] - 1 - e.position["y1"] >= 0:
                hitposy = {"x" : e.position["x1"] + (ele.position["y1"] - e.position["y2"] - 1)*e.speed["x"]/e.speed["y"], "y" : ele.position["y1"] - 1, "dist" : 0, "id": "ceil"}
                hitposy["dist"] = ((hitposy["x"] - e.position["x1"])**2 + (hitposy["y"] - e.position["y1"])**2)**(1/2)
            else:
                hity = False
            #---end if---
            if hitx and (ele.position["y1"]>=hitposx["y"]>ele.position["y2"]-1 or hitposx["y"]>ele.position["y1"]>hitposx["y"]+dy-1):
                hitpoint["x"].append(hitposx)
            #---end if---
            
            if hity and (ele.position["x1"]<=hitposy["x"]<ele.position["x2"]+1 or hitposy["x"]<ele.position["x1"]<hitposy["x"]+dx+1):
                hitpoint["y"].append(hitposy)
            #---end if---
        #---end for---

        hitpointx = []
        for x in hitpoint["x"]:
            if hitpointx == []:
                hitpointx = [x["x"], x["y"], x["dist"], x["id"]]
            elif x["dist"] < hitpointx[2]:
                hitpointx = [x["x"], x["y"], x["dist"], x["id"]]
            #---end if---
        #---end for---

        hitpointy = []
        for y in hitpoint["y"]:
            if hitpointy == []:
                hitpointy = [y["x"], y["y"], y["dist"], y["id"]]
            elif y["dist"] < hitpointy[2]:
                hitpointy = [y["x"], y["y"], y["dist"], y["id"]]
            #---end if---
        #---end for---

        if hitpointx != [] and hitpointy != [] and hitpointx[2] == hitpointy[2]:
            e.speed["x"] = 0
            e.speed["y"] = 0
            e.position["x1"] = hitpointx[0]
            e.position["x2"] = hitpointx[0] + dx
            e.position["y1"] = hitpointy[1]
            e.position["y2"] = hitpointy[1] + dy
            e.hit[hitpointy[3]] = True
            e.hit[hitpointx[3] + "wall"] = True
        elif hitpointx != [] and (hitpointy == [] or hitpointx[2] < hitpointy[2]):
            e.speed["x"] = 0
            e.position["x1"] = hitpointx[0]
            e.position["x2"] = hitpointx[0] + dx
            e.position["y1"] = hitpointx[1]
            e.position["y2"] = hitpointx[1] + dy
            e.hit[hitpointx[3] + "wall"] = True
        elif hitpointy != [] and (hitpointx == [] or hitpointx[2] > hitpointy[2]):
            e.speed["y"] = 0
            e.position["x1"] = hitpointy[0]
            e.position["x2"] = hitpointy[0] + dx
            e.position["y1"] = hitpointy[1]
            e.position["y2"] = hitpointy[1] + dy
            e.hit[hitpointy[3]] = True
        #---end if---
    #---end for---
#---end hit---

def move(ent, obj, zone):
    for e in ent + zone["ent"]:
        e.hit = {"rwall": False, "lwall": False, "floor": False, "ceil": False}
    #---end for---
    hit(ent, obj, zone)
    hit(ent, obj, zone)
    for e in ent + zone["ent"]:
        e.position["x1"] += e.speed["x"]
        e.position["x2"] += e.speed["x"]
        e.position["y1"] += e.speed["y"] 
        e.position["y2"] += e.speed["y"]
    #---end for---
#---end move---

def worldUpdater(world, inp = {"up" : [False], "right": [False], "left": [False]}):
    ent = world.getEntities()
    obj = world.getObjects()
    zone = world.getZones()

    ent[0].updatePlayerInput(inp)
    stateUpdater(ent + zone["ent"], world)
    acceleration(ent + zone["ent"], obj + zone["obj"], world.environment)
    speed(ent + zone["ent"])
    move(ent, obj, zone)
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

def stateUpdater(lists, world):
    for item in lists:
        if item.keyChar == 'm':
            up = False
            down = False
            right = False
            left = False
            for i in lists:
                if i.keyChar == 'c':
                    if i.position["x1"] == item.position["x2"] + 1 and (i.position["y1"] <= item.position["y1"] <= i.position["y2"] or item.position["y1"] <= i.position["y1"] <= item.position["y2"]):
                        right = True
                    elif item.position["x1"] == i.position["x2"] + 1 and (i.position["y1"] <= item.position["y1"] <= i.position["y2"] or item.position["y1"] <= i.position["y1"] <= item.position["y2"]):
                        left = True
                    elif i.position["y2"] == item.position["y1"] + 1 and (i.position["x1"] <= item.position["x1"] <= i.position["x2"] or item.position["x1"] <= i.position["x1"] <= item.position["x2"]):
                        up = True
                    elif item.position["y2"] == i.position["y1"] + 1 and (i.position["x1"] <= item.position["x1"] <= i.position["x2"] or item.position["x1"] <= i.position["x1"] <= item.position["x2"]):
                        down = True
                    #---end if---
                #---end if---
            #---end for---
            if up and down:
                item.updateState('b')
            elif right and left:
                item.updateState('t')
            #---end if---
        elif item.keyChar == 'c':
            up = False
            down = False
            right = False
            left = False
            for i in lists:
                if i.keyChar == 'm' or i.keyChar == 'c':
                    if i.position["x1"] == item.position["x2"] + 1 and (i.position["y1"] <= item.position["y1"] <= i.position["y2"] or item.position["y1"] <= i.position["y1"] <= item.position["y2"]):
                        right = True
                    elif item.position["x1"] == i.position["x2"] + 1 and (i.position["y1"] <= item.position["y1"] <= i.position["y2"] or item.position["y1"] <= i.position["y1"] <= item.position["y2"]):
                        left = True
                    elif i.position["y2"] == item.position["y1"] + 1 and (i.position["x1"] <= item.position["x1"] <= i.position["x2"] or item.position["x1"] <= i.position["x1"] <= item.position["x2"]):
                        up = True
                    elif item.position["y2"] == i.position["y1"] + 1 and (i.position["x1"] <= item.position["x1"] <= i.position["x2"] or item.position["x1"] <= i.position["x1"] <= item.position["x2"]):
                        down = True
                    #---end if---
                #---end if---
            #---end for---
            if up:
                if down:
                    if right:
                        if left:
                            item.updateState("+")
                        else:
                            item.updateState("}")
                        #---end if---
                    else:
                        if left:
                            item.updateState("{")
                        else:
                            item.updateState("b")
                        #---end if---
                    #---end if---
                else:
                    if right:
                        if left:
                            item.updateState("-")
                        else:
                            item.updateState("[")
                        #---end if---
                    else:
                        if left:
                            item.updateState("]")
                        else:
                            item.updateState("'")
                        #---end if---
                    #---end if---
                #---end if---
            else:
                if down:
                    if right:
                        if left:
                            item.updateState("_")
                        else:
                            item.updateState("(")
                        #---end if---
                    else:
                        if left:
                            item.updateState(")")
                        else:
                            item.updateState(",")
                        #---end if---
                    #---end if---
                else:
                    if right:
                        if left:
                            item.updateState("t")
                        else:
                            item.updateState("c")
                        #---end if---
                    else:
                        if left:
                            item.updateState("d")
                        else:
                            item.updateState("default")
                        #---end if---
                    #---end if---
                #---end if---
            #---end if---
        elif item.keyChar == 'f':
            item.sdetector(world.getBoard())
            if item.spot != None:
                item.changeState('default')
                item.state = 'default'
            if item.state == "default":
                item.rjump = int(r.random() * 125)
                if ((lists[0].position["x1"]-item.position["x1"])**2 + (lists[0].position["y1"]-item.position["y1"])**2)**(1/2) <= item.view:
                    item.state = 'attack'
                    if lists[0].position["x1"] < item.position["x1"]:
                        item.changeState('attack_left')
                    else:
                        item.changeState('attack_right')
                    #---end if---
                elif item.rjump == 0 and item.r_spot != None:
                    item.changeState('go_right')
                    item.state = 'jump'
                elif item.rjump == 1 and item.l_spot != None:
                    item.changeState('go_left')
                    item.state = 'jump'
                #---end if---
            elif item.hit["floor"] and item.spot == None:
                item.state = 'ground'
                if item.r_spot != None and item.l_spot != None:
                    distr = item.position["x1"]-item.r_spot.position["x1"]
                    distl = item.position["x1"]-item.l_spot.position["x1"]
                    if (distr < distl or item.position["y1"] < item.l_spot.position["y1"]) and item.position["y1"] >= item.r_spot.position["y1"]:
                        item.changeState('ground_right')
                    elif (distr < distl or item.position["y1"] < item.l_spot.position["y1"]) and item.position["y1"] >= item.r_spot.position["y1"]:
                        item.changeState('ground_left')
                    else:
                        item.changeState('ground')
                    #---end if---
                elif item.r_spot != None:
                    item.changeState('ground_right')
                elif item.l_spot != None:
                    item.changeState('ground_left')
                else:
                    item.changeState('ground')
            #---end if---
        #---end if---
    #---end for---
#---end stateDetection---