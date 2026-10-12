from abc import ABC, abstractmethod

# 1. Abstract base class (Abstraction)
class Animal(ABC):
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    @abstractmethod
    def make_sound(self):
        pass
    
    @abstractmethod
    def move(self):
        pass
    
    # Concrete method
    def eat(self):
        print(f"{self.name} is eating")
    
    def __str__(self):
        return f"{self.name} ({self.species})"

# 2. Intermediate classes (Single Inheritance)
class Mammal(Animal):
    def __init__(self, name, species, fur_color):
        super().__init__(name, species)
        self.fur_color = fur_color
    
    def move(self):
        return "walks on land"

class Bird(Animal):
    def __init__(self, name, species, wing_span):
        super().__init__(name, species)
        self.wing_span = wing_span
    
    def move(self):
        return "flies in the sky"

# 3. Specific animal classes (Single Inheritance)
class Dog(Mammal):
    def __init__(self, name, fur_color="brown"):
        super().__init__(name, "Canine", fur_color)
    
    def make_sound(self):
        return "Woof! Woof!"
    
    def fetch(self):
        return f"{self.name} is fetching the ball!"

class Cat(Mammal):
    def __init__(self, name, fur_color="gray"):
        super().__init__(name, "Feline", fur_color)
    
    def make_sound(self):
        return "Meow!"
    
    def climb(self):
        return f"{self.name} is climbing a tree!"

class Eagle(Bird):
    def __init__(self, name, wing_span=6.5):
        super().__init__(name, "Bird of Prey", wing_span)
    
    def make_sound(self):
        return "Screech!"
    
    def hunt(self):
        return f"{self.name} is hunting from above!"

class Penguin(Bird):
    def __init__(self, name, wing_span=2.0):
        super().__init__(name, "Flightless Bird", wing_span)
    
    def make_sound(self):
        return "Squawk!"
    
    def move(self):
        return "waddles on land and swims in water"
    
    def swim(self):
        return f"{self.name} is swimming gracefully!"

# 4. Multiple Inheritance - Simple version
class FlyingDog(Dog):
    def __init__(self, name, fur_color="golden", wing_span=4.0):
        # Initialize Dog (which handles Animal initialization)
        super().__init__(name, fur_color)
        # Add wing_span attribute from Bird
        self.wing_span = wing_span
    
    def make_sound(self):
        # Get dog sound and create a magical version
        dog_sound = Dog.make_sound(self)
        return f"{dog_sound} *with magical echoes*"
    
    def move(self):
        return "runs on land and flies in the sky"
    
    def special_ability(self):
        return f"{self.name} can fetch balls from the clouds!"

# 5. Polymorphism - Function that works with any animal
def animal_showcase(animal):
    """Demonstrates polymorphism - works with any Animal object"""
    print(f"\n--- Showcasing {animal.name} ---")
    print(f"Species: {animal.species}")
    print(f"Sound: {animal.make_sound()}")
    print(f"Movement: {animal.name} {animal.move()}")
    animal.eat()
    
    # Check for specific attributes/methods using hasattr
    if hasattr(animal, 'fur_color'):
        print(f"Fur color: {animal.fur_color}")
    if hasattr(animal, 'wing_span'):
        print(f"Wing span: {animal.wing_span} feet")
    if hasattr(animal, 'fetch'):
        print(f"Special: {animal.fetch()}")
    if hasattr(animal, 'climb'):
        print(f"Special: {animal.climb()}")
    if hasattr(animal, 'hunt'):
        print(f"Special: {animal.hunt()}")
    if hasattr(animal, 'swim'):
        print(f"Special: {animal.swim()}")
    if hasattr(animal, 'special_ability'):
        print(f"Special: {animal.special_ability()}")

# 6. Main demonstration function
def main():
    print("=== Animal Management System Demo ===")
    
    # Create instances of different animals
    animals = [
        Dog("Buddy", "golden"),
        Cat("Whiskers", "black"),
        Eagle("Soar", 7.0),
        Penguin("Waddles", 1.8),
        FlyingDog("Sky", "white", 5.0)
    ]
    
    # Demonstrate polymorphism
    for animal in animals:
        animal_showcase(animal)
    
    print("\n=== Method Resolution Order Demo ===")
    flying_dog = FlyingDog("Aero")
    print(f"FlyingDog MRO: {[cls.__name__ for cls in FlyingDog.__mro__]}")
    
    print("\n=== Inheritance Chain Demo ===")
    buddy = Dog("Max")
    print(f"Max is instance of Dog: {isinstance(buddy, Dog)}")
    print(f"Max is instance of Mammal: {isinstance(buddy, Mammal)}")
    print(f"Max is instance of Animal: {isinstance(buddy, Animal)}")
    
    print("\n=== Abstract Class Demo ===")
    try:
        # This would raise an error:
        direct_animal = Animal("Generic", "Unknown")
        print("This line should not print")
    except TypeError as e:
        print(f"Error creating Animal directly: {e}")

if __name__ == "__main__":
    main()