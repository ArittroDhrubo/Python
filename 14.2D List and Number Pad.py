Skilled = ["Maraj", "Shadhin", "Galib"]
CGPA = ["Arittro", "Uma", "Osama"]
Sup = ["Amatul", "Tasfiah", "Kaif"]
Gamer = ["Awsaf", "Samin", "Al-Amin"]

Students = [Skilled,CGPA,Sup,Gamer]

print(Students[1][0])
print(Students[3][2])

for x in Students:
    for y in x:
        print(y, end = " ")
    print()

print()

NumPad = ((1,2,3),
          (4,5,6),
          (7,8,9),
          ("*",0,"#"))

for x in NumPad:
    for y in x:
        print(y, end = " ")
    print()