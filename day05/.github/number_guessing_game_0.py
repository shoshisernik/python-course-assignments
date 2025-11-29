import random

def main():
    print("I'm thinking of a number between 1 and 50...")
    secret_number = random.randint(1, 50)

    guess = int(input("Take a guess: "))

    if guess < secret_number:
        print("My number is smaller.")
    elif guess > secret_number:
        print("My number is bigger.")
    else:
        print("You guessed it! Well done!")

if __name__ == "__main__":
    main()