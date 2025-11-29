import random
def main():
    print("I'm thinking of a number between 1 and 50...")
    secret_number = random.randint(1,50)

    user_input = input("Take a guess (or 'x' to quit):")
    
    #if the player wants to quit, they should type 'x'.
    if user_input.lower() == 'x':
        print("game over")
        return  
    # Otherwise, put in an integer between 1 and 50 to guess. 
    try:
        guess = int(user_input)
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 50 or 'x' to quit.")
        return
   
    if guess < secret_number:
        print("My number is smaller.")
    elif guess > secret_number:
        print("My number is bigger.")
    else:
        print("You guessed it! Well done!") 

if __name__ == "__main__":
    main()