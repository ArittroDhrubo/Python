questions = (
        "What is the capital of France?",
        "What is 5 + 7?",
        "Which language is used for web development?",
        "Which planet is known as the Red Planet?",
        "What is the largest ocean on Earth?"
    )

    # Options (each is a tuple of 4 options)
options = (
        ("A. Paris", "B. London", "C. Rome", "D. Berlin"),
        ("A. 10", "B. 12", "C. 13", "D. 11"),
        ("A. Python", "B. C++", "C. JavaScript", "D. Java"),
        ("A. Venus", "B. Earth", "C. Mars", "D. Jupiter"),
        ("A. Atlantic", "B. Indian", "C. Arctic", "D. Pacific")
    )

    # Correct Answers (corresponds to each question)
answers = ("A", "B", "C", "C", "D")

    # To store user's guesses
guesses = []

    # Score counter
score = 0

print("=== Welcome to the Quiz Game ===\n")

    # Loop through each question
for i in range(len(questions)):
        print(f"Q{i+1}: {questions[i]}")
        for opt in options[i]:
            print(opt)

        # Get user guess
        guess = input("Your answer (A/B/C/D): ").strip().upper()
        guesses.append(guess)

        # Check and update score
        if guess == answers[i]:
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Wrong! The correct answer was {answers[i]}.\n")

    # Final results
print("=== Quiz Completed! ===")
print(f"Your score: {score}/{len(questions)}\n")

print("Your guesses: ", guesses)
print("Correct answers:", answers)

    # Performance feedback
if score == len(questions):
        print("🏆 Excellent! You're a quiz master!")
elif score >= 3:
        print("👍 Good job!")
else:
        print("😅 Better luck next time!")


