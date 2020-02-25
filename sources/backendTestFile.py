import backendFunctions as b

a = ["11", "12", "21", "22"]

for i in a:
    print(b.HitboxesFileReader("./files/environment1/level1/boxes" + i + ".dat"))