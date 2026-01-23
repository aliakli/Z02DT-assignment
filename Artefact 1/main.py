#14/01
#Imports
import math

#Global variables
NOT_A_NUMBER = "NaN" 
ANSWER = 0

#Main
def main():
    #Call global ANSWER variable
    global ANSWER
    #Main program loop 
    while True: 
        #Check whether user wants to continue using the calculator, clear memory or exit (strip to remove whitespace and move input to lower case) 
        operation = input("Enter an operand (+,-,*,/), enter 'clr' to delete memory, enter 'ans' to see the answer stored in memory or press enter to exit: ").lower().strip() 
        #End main program loop if requested to 
        if operation == "": 
            print("Goodbye") 
            break
        
        #Store the operation in the variable 'operation'
        operation = handle_operand(operation) 
        if operation == "Not an operand": 
            print("Invalid operand") 
            continue
        elif operation == "clear":
            print(ANSWER)
            continue
        elif operation == "memory":
            continue
        
        #Get user number inputs
        numbers = get_numbers()
        #Assign the first number to answer then remove it from the first element in the array
        ANSWER += 0 if len(numbers) == 0 else numbers.pop(0)
        #Perform the operation on the numbers stored in 'numbers'
        #Display to output the result
        if operation(numbers) == "Division by zero":
            print("Division by zero")
            ANSWER = 0
        else:
            print(ANSWER) 

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

#Function to decide which operand is being requested 
def handle_operand(operand): 
    #Using a variety of ways people may ask for an operator to account for the broadest amount of users
    global ANSWER
    match operand:
        case "mem" | "memory" | "ans" | "answer":
            print(ANSWER)
            return "memory"
        case "cls" | "clear" | "clr" | "del":
            ANSWER = 0
            return "clear"
        case "add" | "addition" | "a" | "+": 
            return addition 
        case "sub" | "subtraction" | "s" | "-" | "subtract": 
            return subtraction 
        case "multiply" | "mult" | "m" | "*" | "multiplication": 
            return multiplication 
        case "division" | "div" | "d" | "/" | "divide": 
            return division 
        case _: 
            return "Not an operand" 

#Function to add an array of inputs 
def addition(lst):
    global ANSWER
    #Output (n+(n+1)+(n+2)...)
    print(ANSWER,"+"," + ".join("{0}".format(n) for n in lst))
    ANSWER += sum(lst)

#Function to subtract 2 inputs 
def subtraction(lst):
    global ANSWER
    #Output (n-(n+1)-(n+2)...)
    print(ANSWER,"-"," - ".join("{0}".format(n) for n in lst))
    ANSWER -= sum(lst)

#Function to divide 2 inputs 
def division(lst):
    global ANSWER
    try:
        #Output (n/(n+1)/(n+2)...)
        print(ANSWER,"/"," / ".join("{0}".format(n) for n in lst))
        for number in lst:
            ANSWER /= number
        ANSWER = validate_number(ANSWER) 
    #To prevent the program from crashing, this exception catches the ZeroDivisionError and returns the string 
    except ZeroDivisionError:
        return "Division by zero" 

  

#Function to multiply 2 inputs 
def multiplication(lst):
    global ANSWER
    #Output (n*(n+1)*(n+2)...)
    print(ANSWER,"*"," * ".join("{0}".format(n) for n in lst))
    for number in lst:
        ANSWER *= number


#Prevents the program from being ran when imported (probably will use this with OOP) 
if __name__ == "__main__": 
    main() 