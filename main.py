# 30/01

# Imports
from bidmas import Calculator
import os


def load_creds():
    creds = {}
    if os.path.exists("creds.txt"):
        with open("creds.txt", "r") as f:
            for line in f:
                username, password = line.strip().split(":")
                creds[username] = password
    return creds


def save_cred(username, password):
    with open("creds.txt", "a") as f:
        f.write(f"{username}:{password}\n")


def main():
    instance = Calculator()
    creds = load_creds()
    logged_in = False

    while not logged_in:
        print("\n1. Login")
        print("2. Register")
        choice = input("Choose an option: ")

        username = input("Enter username: ")
        password = input("Enter password: ")

        if choice == "1":
            if username in creds and creds[username] == password:
                print("Login successful!")
                logged_in = True
            else:
                print("Invalid username or password.")

        elif choice == "2":
            if username in creds:
                print("Username already exists.")
            else:
                save_cred(username, password)
                creds[username] = password
                print("Account created! You are now logged in.")
                logged_in = True
        else:
            print("Invalid option.")

    while True:
        expression = input(
            "Enter expression, type exit to close or type mode to change mode:\n"
        )

        if expression.lower() == "exit":
            break

        if expression.lower() == "mode":
            instance.angle_mode = not instance.angle_mode
            print("Radians" if instance.angle_mode else "Degrees")
        else:
            print(instance.tokenise_expression(expression))


if __name__ == "__main__":
    main()
