Name = "Bro"
print("Hello" + " " + Name)
operator = input("Enter Operator ( + / - / * / % / (/) ): ")

num1 = float(input("Enter Number-1: "))
num2 = float(input("Enter Number-2: "))

if operator == "+":
    result = num1 + num2
    print(f"Result: {result}")

elif operator == "-":
    result = num1 - num2
    print(f"Result: {result}")

elif operator == "*":
    result = num1 * num2
    print(f"Result: {result}")

elif operator == "/":
    result = num1 / num2
    print(f"Result: {result}")

elif operator == "%":
    result = num1 % num2
    print(f"Result: {result}")

else:
    print(f"{operator} is not a valid operator.")

Status = "Passed" if result > 60 else "Failed"

print(Status)

