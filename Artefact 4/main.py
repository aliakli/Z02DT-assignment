#Imports
from bidmas import Calculator  # Import calculator class
from login import Login  # Import login management
from dbmanager import UserManagement  # Import database management
import csv  # For exporting calculation logs
from test_calculator import TestCalculator  # For admin testing

class CalcLogs:
    """Handles storing and exporting calculation logs."""
    def __init__(self):
        self.UM = UserManagement("users")  # Initialize user management
    
    def add_to_db(self, user, expression, mode, error = None):
        self.UM.add_calculation_logs(user, expression, mode, errors = error)  # Add a calculation log

    def export(self):
        with open("calculation_logs.csv" ,"w", newline = "") as file:
            calculations = self.UM.get_calculation_logs()  # Fetch all logs
            writer = csv.writer(file)
            writer.writerow(["Username", "Expression","Mode", "Errors", "Timestamp"])  # Write header
            writer.writerows(calculations)  # Write all calculation logs
            
#Main
def main():
    """Runs the main calculator loop with login and logging functionality."""
    instance = Calculator()  # Create calculator instance
    
    logs = CalcLogs()  # Create logs handler
    login = Login()  # Perform login
    user = login.user  # Get logged-in user
    isLoggedIn = login.isLoggedIn  # Check if user is logged in
    isAdmin = login.isAdmin  # Check if user is admin
    mode = "Radians"  # Default angle mode
    
    while True:  # Main loop
        if not isLoggedIn:
            break  # Exit if not logged in
        
        expression = input("Enter expression, type exit to close or type mode to change mode:\n")
        
        if expression.lower().strip() == "test" and isAdmin:
            test = TestCalculator()  # Run calculator tests for admin
            test.test_calculator()
            continue
            
        if expression.lower().strip() == "exit" or expression.lower().strip() == "close":
            break  # Exit program
        elif expression.lower().strip() == "mode":
            instance.angle_mode = not instance.angle_mode  # Toggle angle mode
            print("Radians" if instance.angle_mode else "Degrees")
            mode = "Degrees" if mode == "Radians" else "Radians"
        elif expression.lower().strip() == "degrees":
            instance.angle_mode = False  # Set mode to degrees
            print("Degrees")
            mode = "Degrees"
        elif expression.lower().strip() == "radians":
            instance.angle_mode = True  # Set mode to radians
            print("Radians")
            mode = "Radians"
        else:
            try:
                # Evaluate expression and print result
                result = instance.tokenise_expression(expression.lower().strip().replace("^","**"))
                print(result)
                logs.add_to_db(user, f"{expression.lower().strip()}={result}", mode)  # Log calculation
            except Exception as err:
                if len(expression.lower().strip()) > 0 and not expression[0].lower().strip().isdigit():
                    print("Invalid syntax")  # Syntax error
                    logs.add_to_db(user, f"{expression.lower().strip()}", mode, error = "Syntax Error")
                    continue
                print("Error "+str(err))  # Other errors
                logs.add_to_db(user, f"{expression.lower().strip()}",mode ,error = str(err))
                
#Prevents the program from being ran when imported
if __name__ == "__main__":
    main()  # Run main loop
    logs = CalcLogs()  # Export logs after program ends
    logs.export()  # Save logs to CSV
