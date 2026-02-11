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
    user = login.user
    isLoggedIn = login.isLoggedIn
    isAdmin = login.isAdmin
    while True:
        if not isLoggedIn:
            break
        calculation_logs = open("calculation_logs.txt", "a")
        expression = input("Enter expression, type exit to close or type mode to change mode:\n")
        if expression.lower().strip() == "test" and isAdmin:
            pass
        if expression.lower().strip() == "exit" or expression.lower().strip() == "close":
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
            try:
                print(instance.tokenise_expression(expression.lower().strip().replace("^","**")))
                calculation_logs.write(f"{user}: {expression}={instance.tokenise_expression(expression.lower().strip().replace('^','**'))}\n")
            except:
                if len(expression.lower().strip()) > 0 and not expression[0].lower().strip().isdigit():
                    print("Invalid syntax")
                    calculation_logs.write(f"{user}: {expression} [Invalid]\n")
                    continue
                    print("Error")
                    calculation_logs.write(f"{user}: {expression} [Error]\n")
        
            
            
#Prevents the program from being ran when imported
if __name__ == "__main__":
    with open("calculation_logs.txt", "a") as calculation_logs:
        main()
