import random

print("🎯 Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")

# Random number between 1 and 100
high = 100
low = 1
secret_number = random.randint(low, high)
    
attempts = 0

while True:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1

            if guess < low or guess > high:
                print("Please guess a number between 1 and 100.")
                continue

            if guess == secret_number:
                print(f"🎉 Congratulations! You guessed the number in {attempts} attempts.")
                break
            elif guess < secret_number:
                print("🔼 Too low. Try again.")
            else:
                print("🔽 Too high. Try again.")

        except ValueError:
            print("❗ Please enter a valid number.")


