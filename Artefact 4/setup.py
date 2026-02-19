from dbmanager import UserManagement,Database

class Setup:
    def setup(self):
        Database().create_database("users")  # Ensure database exists
        self.UM = UserManagement("users")  # Connect to user DB
        self.UM.create_calculation_logs()  # Create calculations table
        