import datetime  # For timestamps
import mysql.connector  # For MySQL database operations

# Class to log events to a text file
class Logs:
    def log_change(change, user="admin"):
        logs = open("log.txt", "a")  # Open log file in append mode
        now = datetime.datetime.today().replace(microsecond=0)  # Current timestamp
        logs.write(f"{user}: {change}: {now}\n")  # Write log entry
        logs.close()  # Close file

# Base class for database connection and table management
class Database:
    def __init__(self, target_database=None, aka="admin"):
        self.host = "localhost"  # DB host
        self.user = "root"  # DB username
        self.password = "C0ventryCUC"  # DB password
        self.cursor = None
        self.db = None
        self.aka = aka  # User performing DB operations

        if not self.__connect(target_database, aka):  # Connect to DB
            print(f"failed to connect to {target_database}")
            return
        else:
            self.cursor = self.db.cursor()
            Logs.log_change("Connected to database", user=aka)

    def create_database(self, name):
        cursor = self.cursor
        cursor.execute("SHOW DATABASES")  # Get existing databases
        if name not in cursor:
            try:
                cursor.execute(f"CREATE DATABASE {name}")  # Create DB
                Logs.log_change(f"Created database called {name}", user="admin")
            except:
                print(f"database '{name}' could not be created")

    def _create_table(self, table_name, *columns):
        cursor = self.cursor
        cursor.execute("SHOW TABLES")  # Get existing tables
        tables = [row[0] for row in cursor.fetchall()]
        if table_name in tables:  # Skip if table exists
            return False

        columns_sql = ", ".join(columns)  # Format column definitions
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name}
        ({columns_sql})
        ENGINE = InnoDB
        """
        self.cursor.execute(query)  # Create table
        Logs.log_change(f"Created table called {table_name}", user="admin")

    def __connect(self, target_database, users="admin"):
        try:
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=target_database
            )
            Logs.log_change(
                f"Successfully connected to database {target_database}",
                user=users
            )
            return True
        except mysql.connector.Error as err:
            print("MySQL error:", err)  # Print connection error
            Logs.log_change(
                f"Failed to connect to database {target_database}",
                user="admin"
            )
            raise ValueError(f"Unable to connect to {target_database}")
            return False

# Class to manage users and calculation logs
class UserManagement(Database):
    def __init__(self, aka="system"):
        super().__init__("users", aka)  # Connect to users DB
        self.__create_user_table()  # Ensure user table exists
        self.aka = aka

    def __create_user_table(self):
        cursor = self.cursor
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        if "users" in tables:  # Skip if table exists
            return
        
        super()._create_table(
            "users",
            "id INT AUTO_INCREMENT PRIMARY KEY",
            "name VARCHAR(255) NOT NULL UNIQUE",
            "userpass VARCHAR(255) NOT NULL",
            "role VARCHAR(255) DEFAULT 'visitor'",
            "added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        )
        
        self.create_user("admin", "admin", "admin")
        Logs.log_change("Created user table", user="admin")
        
    def create_user(self, username, password, role="visitor"):
        roles = ["visitor", "admin", "test"]
        if role not in roles:  # Validate role
            raise Exception("Invalid role")
        value = (username, password, role)
        query = "INSERT INTO users (name, userpass, role) VALUES (%s,%s,%s)"
        self.cursor.execute(query, value)  # Add user
        self.db.commit()
        Logs.log_change(f"Created new user {username} with role {role}", user="admin")

    def delete_user(self, username, executer="admin"):
        self.cursor.execute(f"DELETE FROM users WHERE name = '{username}'")  # Delete user
        self.db.commit()
        Logs.log_change(f"Deleted user {username}", user=executer)

    def get_users(self):
        self.cursor.execute("SELECT name, userpass, role FROM users")  # Fetch all users
        Logs.log_change("Requested all users", user="admin")
        return self.cursor.fetchall()

    def validate_user_login(self, user, password):
        self.cursor.execute(f"SELECT name, userpass from users WHERE name = %s", (user,))
        detail = self.cursor.fetchone()
        if detail is None or detail[1] != password:  # Check credentials
            return False
        else:
            return True

    def set_password(self, user, old_password, new_password):
        self.cursor.execute(f"SELECT name, userpass from users WHERE name = %s", (user,))
        detail = self.cursor.fetchone()
        if old_password != detail[1]:  # Verify old password
            return False
        self.cursor.execute(f"UPDATE users SET userpass = %s WHERE name = %s", (new_password, user))
        self.db.commit()
        return True

    def create_calculation_logs(self):
        # Create table for storing calculation history
        super()._create_table(
            "calculations",
            "id INT AUTO_INCREMENT PRIMARY KEY",
            "userid INT NOT NULL",
            "expression TEXT NOT NULL",
            "mode TEXT NOT NULL",
            "errors TEXT",
            "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "FOREIGN KEY (userid) REFERENCES users(id) ON DELETE CASCADE"
        )

    def add_calculation_logs(self, user, expression, mode, errors=None):
        try:
            self.cursor.execute("SELECT id from users WHERE name = %s",(user,))
            result = self.cursor.fetchone()
            if result is None:
                return False
            userid = result[0]
            value = (userid, expression, mode, errors)
            query = "INSERT INTO calculations (userid, expression, mode,errors) VALUES (%s,%s,%s,%s)"
            self.cursor.execute(query, value)  # Add calculation record
            self.db.commit()
            return True
        except:
            return False

    def get_calculation_logs(self):
        self.cursor.execute("SELECT userid, expression, mode,errors, timestamp FROM calculations")  # Fetch logs
        return self.cursor.fetchall()
    
    def get_userid(self, user):
        self.cursor.execute("SELECT id from users WHERE name = %s",(user,))
        result = self.cursor.fetchone()
        return result[0] if result else None
# Initialize database and tables when run directly
if __name__ == "__main__":
    Database().create_database("users")  # Ensure database exists
    UM = UserManagement("users")  # Connect to user DB
    UM.create_calculation_logs()  # Create calculations table
