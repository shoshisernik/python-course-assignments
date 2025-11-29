import random
def main():
    print("I'm thinking of a number between 1 and 50...")
    secret_number = random.randint(1,50)
    while True: #this will allow multiple guesses until the player gets it right or stops guessing. 
        user_input = input("Take a guess (or 'x' to quit):")
    
        if user_input.lower() == 'x':   #if the player wants to quit, they should type 'x'.
            print("game over")
            return 
        if user_input.lower() == 's':  #if the player wants the answer, they should type 's'.
            print(f"The secret number is: {secret_number}")
            return
        if user_input.strip() == "":
            print("Please enter a guess, 's' to reveal the secret number, or 'x' to quit.")
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


if __name__ == "__main__":
    main()