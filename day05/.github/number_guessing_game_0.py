#This is the basic version of the number guessing game. The player has to guess a number between 1 and 50. After each guess, the program will tell the player if the secret number was higher or lower than the guess.

import random

def main():
    print("I'm thinking of a number between 1 and 50...")
    secret_number = random.randint(1, 50)

    guess = int(input("Take a guess: "))

    if guess < secret_number:
        print("My number is bigger.")
    elif guess > secret_number:
        print("My number is smaller.")
    else:
        print("You guessed it! Well done!")

if __name__ == "__main__":
    main()