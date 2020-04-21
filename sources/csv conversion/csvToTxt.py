try:
	name = input("enter the file name: ")
	with open(name+".csv", 'r') as file:
		contents = file.read()
	#---end with---

	print(contents)
	tab = contents[0] if contents[0] != ";" else "."

	for i in range(1,len(contents)):
		if contents[i] == ";" and contents[i-1] == ";":
			tab += " "
		elif contents[i] != ";":
			tab += contents[i]
		#---end if---
	#---end for---
	print(tab)

	with open(name+".txt", "w") as file:
		file.write(tab)
	#---end with---

	with open(name+".txt", "r") as file:
		print(file.read())
	#---end with---
except FileNotFoundError as e:
	raise e
#---end try---

o=1
while o:
	o = input("end")
#---end while---