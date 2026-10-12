#List Duplicates are allowed, Ordered and Changable
#Set Duplicates are not allowed, Unordered and immutable
#tuple Duplicates are allowed, Faster and Ordered

Bokachoda = ["Ashraful", "Kaif", "Faez", "Salim", "Rasel"]

print(Bokachoda[1])

New_Bokachoda = ""

while(New_Bokachoda != "Done"):
    New_Bokachoda = input("Ener the name of Bokachoda: ")
    Bokachoda.append(New_Bokachoda)

Bokachoda.insert(0,"Saplaful")
print(len(Bokachoda))
print(Bokachoda)
print("Ashraful" in Bokachoda)
Bokachoda.remove("Salim")
Bokachoda.sort()
print(Bokachoda)
print(Bokachoda.index("Faez"))
print(Bokachoda.count("Ashraful"))
Bokachoda.reverse()
print(Bokachoda)
Bokachoda.clear()
print(Bokachoda)

Oridemy = {"Maraj", "Marjan", "Arittro", "Salman"}
Oridemy.add("Abir")
Oridemy.add("Maraj")
Oridemy.remove("Salman")
print(Oridemy)
Oridemy.pop()
print(Oridemy)

NSUCirc = ("Arittro","Uma","Shadhin","Tasfiah","Samnin")
print(NSUCirc.index("Shadhin"))
print(NSUCirc.count('Uma'))

for x in NSUCirc:
    print(x)