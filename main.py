#30/01
#Imports
from bidmas import Calculator
from login import Login
#from test import TestCalculator
#Global variables

#Main
def main():
    instance = Calculator()
    #test = TestCalculator()
    
    login = Login()
    isLoggedIn = login.isLoggedIn
    isAdmin = login.isAdmin
    while True:
        if not isLoggedIn:
            break
        expression = input("Enter expression, type exit to close or type mode to change mode:\n")
        if expression.lower().strip() == "test" and isAdmin:
            pass
        if expression.lower().strip() == "exit":
            break
        elif expression.lower().strip() == "mode":
            instance.angle_mode = not instance.angle_mode
            print("Radians" if instance.angle_mode else "Degrees")
        elif expression.lower().strip() == "degrees":
            instance.angle_mode = False
            print("Degrees")
        elif expression.lower().strip() == "radians":
            instance.angle_mode = True
            print("Radians")
        else:
            print(instance.tokenise_expression(expression.replace("^","**")))
            
#Prevents the program from being ran when imported
if __name__ == "__main__": 
    main() 