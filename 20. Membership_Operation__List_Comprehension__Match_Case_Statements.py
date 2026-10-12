#Membership in a List

fruits = ['apple', 'banana', 'mango']

print('apple' in fruits)      # True
print('grape' not in fruits)  # True

#Membership in a String

word = "hello world"

print('h' in word)       # True
print('z' not in word)   # True

#Membership in a Tuple

numbers = (10, 20, 30)

print(20 in numbers)      # True
print(40 not in numbers)  # True

#Membership in a Set

colors = {'red', 'green', 'blue'}

print('green' in colors)        # True
print('yellow' not in colors)   # True

#Membership in a Dictinary
student = {'name': 'Alice', 'age': 16}

print('name' in student)         # True (checks keys)
print('Alice' in student)        # False (values not checked)
print('Alice' in student.values())  # True

#new_list = [expression for item in iterable if condition]

# Squares of numbers from 1 to 5
squares = [x**2 for x in range(1, 6)]
print(squares)  # [1, 4, 9, 16, 25]

# Even numbers from a list
nums = [1, 2, 3, 4, 5, 6]
evens = [x for x in nums if x % 2 == 0]
print(evens)  # [2, 4, 6]

# Match_Case Statements

def get_day(number):
    match number:
        case 1:
            return "Monday"
        case 2:
            return "Tuesday"
        case 3:
            return "Wednesday"
        case 4:
            return "Thursday"
        case 5:
            return "Friday"
        case 6:
            return "Saturday"
        case 7:
            return "Sunday"
        case _:
            return "Invalid input"


num = int(input("Enter a number (1-7): "))
print(get_day(num))

#Problem-2

def is_weekend(day_number):
    match day_number:
        case 6 | 7:
            return True
        case 1 | 2 | 3 | 4 | 5:
            return False
        case _:
            return False

num = int(input("Enter a day number (1-7): "))
if is_weekend(num):
    print("It's the weekend!")
else:
    print("It's a weekday or invalid input.")
