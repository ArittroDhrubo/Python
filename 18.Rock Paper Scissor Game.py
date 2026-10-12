import random


print("Welcome to Rock, Paper, Scissors Game!")
print("Type rock, paper, or scissors to play. Type quit to stop the game.")

while True:
        # Get user's choice
        user = input("Your choice: ").lower()

        if user == "quit":
            print("Thanks for playing!")
            break

        if user != "rock" and user != "paper" and user != "scissors":
            print("Please enter a valid choice.")
            continue

        # Get computer's choice
        computer = random.choice(["rock", "paper", "scissors"])
        print(f"Computer chose: {computer}")

        # Decide the winner
        if user == computer:
            print("It's a draw!")
        elif user == "rock" and computer == "scissors":
            print("You win!")
        elif user == "paper" and computer == "rock":
            print("You win!")
        elif user == "scissors" and computer == "paper":
            print("You win!")
        else:
            print("You lose!")


