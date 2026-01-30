#30/01
#Imports
from bidmas import Calculator
#Global variables
#Main
def main():
    while True:
        instance = Calculator()
        expression = input("Enter expression or type exit to close:\n")
        if expression != "exit":
            print(instance.tokenise_expression(expression))
        else:
            print("Goodbye...")
            break
#Prevents the program from being ran when imported (probably will use this with OOP) 
if __name__ == "__main__": 
    main() 