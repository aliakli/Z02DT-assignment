#14/01
#Imports
from operators import Operators
from NumberValidation import NumberValidation
#Global variables



#Main
def main():
    operators = Operators()
    valid_nums = NumberValidation()

    while True:
        operation = input("Enter an operator (+,-,*,/), enter 'clr' to delete memory,\nenter 'ans' to see the answer stored in memory or press enter to exit: ").lower().strip()
        if operation == "":
            print("Goodbye")
            break
        operation = handle_operator(operation, operators)
        if operation == "Not an operator":
            print("Invalid operator")
            continue
        elif operation is None:
            continue
        numbers = valid_nums.get_numbers()
        if len(numbers) > 0:
            operators.answer += numbers.pop(0)
        result = operation(numbers)
        if result == "Division by zero":
            print(result)
            operators.clear()
        else:
            print(operators.answer)
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
        case "exp" | "exponentiation" | "power" | "^" | "**":
            return operators.exponentiation
        case "sin" | "sine":
            return operators.sine
        case "cos" | "cosine":
            return operators.cosine
        case "tan" | "tangent":
            return operators.tangent
        case _: 
            return "Not an operator" 

#Prevents the program from being ran when imported (probably will use this with OOP) 
if __name__ == "__main__": 
    main() 
