Name = 'Arittro Dhrubo'
Age = 23
CGPA = 3.83
Student = True

print(type(Name))
print(type(Age))
print(type(CGPA))
print(type(Student))

Name = bool(Name)
print(type(Name))

Name1 = ""
Name1 = bool(Name1)
print(Name1)

CGPA = int(CGPA)
print(type(CGPA))
print(CGPA)

Student = str(Student)
print(type(Student))
print(Student)

Age = float(Age)
print(Age)
print(type(Age))

#Implicit Typecasting

a = 9
b = 3.0
a = a/b;
print(f"Result: {a}")
print(type(a))