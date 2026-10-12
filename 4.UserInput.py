#Ex-1

Type = input("Enter Character Type: ")
Adjective = input("Enter Designation: ")
Noun = input("Enter name: ")
Age = input("Enter age: ")
print(type(Age))
Age = int(Age)
print(type(Age))
CGPA = float(input("Enter CGPA: "))

print(f"Naturally, I am a very {Type} person")
print(f"Then I met {Adjective} {Noun}")
print(f"Which Motherfucker is {Age} years old")
Age = Age + 1
print(f"After his next Birthday, he becomes {Age}")
print(f"His CGPA is {CGPA}")
CGPA = CGPA + 0.05
print(f"But hopefully after this semester, he will gain {CGPA}")

#Ex-2

length = input("Enter length: ")
length = float(length)
width = input("Enter Width: ")
width = float(width)
height = float(input("Enter Width: "))

volume = length * width * height

#print(f"Volume of the bottle is {volume}")

print(f"Volume of the bottle is {round(volume,2)}")