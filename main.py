#14/01
#Imports
from operators import Operators
#Global variables
NOT_A_NUMBER = "NaN" 
operators = Operators()


#Main
def main():
    operators = Operators()

    while True:
        operation = input("Enter an operand (+,-,*,/), enter 'clr' to delete memory,\nenter 'ans' to see the answer stored in memory or press enter to exit: ").lower().strip()
        if operation == "":
            print("Goodbye")
            break
        operation = handle_operator(operation, operators)
        if operation == "Not an operand":
            print("Invalid operand")
            continue
        numbers = get_numbers()
        if len(numbers) > 0:
            operators.answer += numbers.pop(0)
        result = operation(numbers)
        if result == "Division by zero":
            print(result)
            operators.clear()
        else:
            print(operators.answer)
#Gets the validated numbers from the user input then stores them in an array
def get_numbers():
    numbers = []
    #Loops until the final input is '='
    while True:
        #Add the validated number to the end of the list
        numbers.append(get_valid_number())
        #Checks if the last value in the array is '='
        if numbers[-1] == "=":
            #Remove the '='
            numbers.pop()
            break
    #Return the array
    return numbers
            
#Gets number from user input and validates     
def get_valid_number():
    num = input("Enter a number and press '=' to compute: ")
    #Loops until valid number is given
    while validate_number(num) == NOT_A_NUMBER:
        num = input("Not a valid number\nEnter a number: ")
    return validate_number(num)

#Function to validate number 
def validate_number(inp):
    if inp == "=":
        return "="
    else:
        try: 
            a = float(inp)
            return int(a) if a.is_integer() else a
        except ValueError: 
            #If a number given is not a valid number, this prevents the program from crashing 
            return NOT_A_NUMBER 

#Function to decide which operator is being requested 
def handle_operator(operator,operators): 
    #Using a variety of ways people may ask for an operator to account for the broadest amount of users
    match operator:
        case "mem" | "memory" | "ans" | "answer":
            print(operators.memory())
            return None
        case "cls" | "clear" | "clr" | "del":
            operators.clear()
            return None
        case "add" | "addition" | "a" | "+": 
            return operators.add 
        case "sub" | "subtraction" | "s" | "-" | "subtract": 
            return operators.subtraction 
        case "multiply" | "mult" | "m" | "*" | "multiplication": 
            return operators.multiplication 
        case "division" | "div" | "d" | "/" | "divide": 
            return operators.division 
        case _: 
            return "Not an operator" 

#Prevents the program from being ran when imported (probably will use this with OOP) 
if __name__ == "__main__": 
    main() 
