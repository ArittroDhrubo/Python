# Example: Student Information
# dictionary_Variable = {Keys : Values}
student = {
    "name": "Alice",
    "age": 16,
    "grade": "10th",
    "subjects": ["Math", "English", "Science"]
}

print(student["name"])       # Output: Alice
print(student["subjects"])   # Output: ['Math', 'English', 'Science']
print(student.get("email"))  # Output: Not found

student.update({"email" : "aliceinborla@gmail.com"})

print(student)
student.pop("grade")
print(student)

for key in student:
    print(key, ":", student[key])

print(student.keys())     # All keys
print(student.values())   # All values
print(student.items())    # All key-value pairs

for key, value in student.items():
    print(f"{key}: {value}")

