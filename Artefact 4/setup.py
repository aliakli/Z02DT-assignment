from dbmanager import UserManagement,Database


if __name__ == "__main__":
    Database().create_database("users")  # Ensure database exists
    UM = UserManagement("users")  # Connect to user DB
    UM.create_calculation_logs()  # Create calculations table