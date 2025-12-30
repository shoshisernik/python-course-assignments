#This version of the game is the same as the previous version, but in this version, the player can continue to guess until they get the number correct.

import random

def main():
    print("I'm thinking of a number between 1 and 50...")
    secret_number = random.randint(1, 50)
    while True: #this will allow multiple guesses until the player gets it right or stops guessing.
        guess = int(input("Take a guess: "))

        if guess < secret_number:
            print("My number is bigger.")
        elif guess > secret_number:
            print("My number is smaller.")
        else:
            print("You guessed it! Well done!")
            break #once the player guesses correctly, the loop ends.

if __name__ == "__main__":
    main()