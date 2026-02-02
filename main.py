#30/01
#Imports
from bidmas import Calculator
#Global variables

#Main
def main():
    instance = Calculator()
    while True:
        
        expression = input("Enter expression, type exit to close or type mode to change mode:\n")
        if expression.lower() == "exit":
            break
        elif expression.lower() == "mode":
            instance.angle_mode = not instance.angle_mode
            print("Radians" if instance.angle_mode else "Degrees") 
        else:
            print(instance.tokenise_expression(expression))
        
#Prevents the program from being ran when imported
if __name__ == "__main__": 
    main() 