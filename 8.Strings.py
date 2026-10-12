name = input("Enter your name: ")

result = len(name)

print(f"Length: {result} ")

result = name.find("D")

print(result)

result = name.rfind("D")
print(result)

result = name.capitalize()
print(result)

result = name.upper()
print(result)

result = name.lower()
print(result)

result = name.isdigit()
print(result)

result = name.isalpha()
print(result)

phone_no  = input("Enter your Phone Number: ")

result = phone_no.count("-")
print(result)

result = phone_no.replace("-", "")
print(result)

#Problem-1

if len(name) > 16:
    print("Username can't contain more than 16 characters.")

elif not name.find("-") == -1:
    print("it can't contain space.")

elif not name.isalpha():
    print("it can't contain digits.")

else:
    print(f"Welcome {name}")