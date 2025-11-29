#This version of the game includes all of the previous features, including the addition of the 'n' command, which allows the player to start a new game.
#this version will also generate a new secret number at the end of each round, until the payer decides to quit the game.

import random
DEBUG = True 
Move_mode = True

def main():
    global DEBUG
    global Move_mode

    print("I'm thinking of a number between 1 and 50...")

    while True: #outer loop to allow multiple games until the player decides to quite.
        secret_number = random.randint(1,50)
        while True: #this will allow multiple guesses until the player gets it right or stops guessing. 
            if DEBUG:
                print(f"[DEBUG] Secret number is: {secret_number}")
            if Move_mode:
                print("Moving mode is enabled. The secret number will change +/- 2 after each guess.")

            user_input = input("Take a guess (or 'x' to quit and end gameplay, 's' to reveal secret number and end gameplay, 'm' to turn on Move Mode, or 'n' to generate a new number within your current game. A new game will start after you guess correctly, until you end gameplay.):")
        
            if user_input.lower() == 'x':   #if the player wants to quit, they should type 'x'.
                print("game over")
                return 
            if user_input.lower() == 's':  #if the player wants the answer, they should type 's'.
                print(f"The secret number is: {secret_number}")
                return
            if user_input.strip() == "":
                print("Please enter a guess, 's' to reveal the secret number, or 'x' to quit.")
                continue   
            if user_input.lower() == 'd': #if the player wants to toggle debug mode, they should type 'd'.
                DEBUG = not DEBUG
                state = "ON" if DEBUG else "OFF"
                print(f"Debug mode is now {state}.")
                continue

            if user_input.lower() == 'm': #if the player wants to toggle moving mode, they should type 'm'.
                Move_mode = not Move_mode
                state_move = "ON" if Move_mode else "OFF"
                print(f"Moving mode is now {state_move}.")
                continue
            if user_input.lower() == 'n': #if the player wants to start a new game, they should type 'n'.
                secret_number = random.randint(1,50)
                print("Starting a new game!")
                continue

            try: # Otherwise, put in an integer between 1 and 50 to guess.
                guess = int(user_input)
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 50, 's' to reveal the secret number, or 'x' to quit.")
                continue 
        
            if guess < secret_number:
                print("My number is bigger.")
            elif guess > secret_number:
                print("My number is smaller.")
            else:
                print("You guessed it! Well done!") 
                break #once the player guesses correctly, the game will end (the loop ends).
            if Move_mode:
                secret_number = secret_number + random.choice([-2, -1, 0, 1, 2])

if __name__ == "__main__":
    main()