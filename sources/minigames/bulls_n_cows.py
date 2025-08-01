import random


def check_guess(secret_number, number: str) -> tuple[int, int]:
    secret_number_str = str(secret_number)

    unique_digits = set([n for n in number])
    bulls = sum([min(number.count(digit), secret_number_str.count(digit))
                for digit in unique_digits])
    cows = sum([1 for i in range(len(number)) if (
        number[i] == secret_number_str[i])])

    return bulls, cows


def play_bulls_n_cows():
    print("Bulls and Cows")
    print("4-digit secret number has been generated. Try to guess it.")
    print("Bulls - digits exist in secret number")
    print("Cows - digits match the secret number")

    secret_number = random.randint(1000, 9999)

    while True:
        user_guess = input("Enter number (or 0 to exit):\n>>")
        if user_guess == "0":
            break

        if (not user_guess.isdigit()) or (len(user_guess) != 4):
            print("Please enter 4-digit number.")
            continue

        bulls, cows = check_guess(secret_number, user_guess)
        print(f"Bulls: {bulls}, Cows: {cows}")

        if cows == len(str(secret_number)):
            print("You win!")
            break
