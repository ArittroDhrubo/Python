def greet(name="Guest"):
    print(f"Hello, {name}!")

greet("Alice")   # Output: Hello, Alice!
greet()          # Output: Hello, Guest!

def student_info(name, age, grade):
    print(f"Name: {name}, Age: {age}, Grade: {grade}")

student_info("Tom", 15, "9th")                    # Positional
student_info(age=14, name="Lily", grade="8th")    # Keyword

def register(name, course="Python", level="Beginner"):
    print(f"{name} has enrolled in {course} course at {level} level.")

register("John")  # Uses default course and level
register("Amy", "Java")  # Uses default level
register(name="Sara", course="C++", level="Advanced")  # All keyword
