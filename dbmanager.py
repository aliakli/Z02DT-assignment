import datetime
import mysql.connector


class Logs:
    def log_change(change, user = "admin"):
        logs = open("log.txt", "a")
        now = datetime.datetime.today().replace(microsecond=0)
        logs.write(f"{user}: {change}: {now}\n")
        logs.close()


class Database:
    def __init__(self, target_database = None, aka = "admin"):
        self.host = "localhost"
        self.user = "root"
        self.password = "C0ventryCUC"
        self.cursor = None
        self.db = None
        self.aka = aka

        if not self.__connect(target_database, aka):
            print(f"failed to connect to {target_database}")
            return
        else:
            self.cursor = self.db.cursor()
            Logs.log_change("Connected to database", user = aka)
            # test
            # self.__create_database("johnCena")

    def create_database(self, name):
        cursor = self.cursor
        cursor.execute("SHOW DATABASES")
        if name not in cursor:
            try:
                cursor.execute(f"CREATE DATABASE {name}")
                Logs.log_change(f"Created database called {name}", user = "admin")
            except:
                print(f"database '{name}' could not be created")

    def _create_table(self, table_name, *columns):
        cursor = self.cursor

        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]

        if table_name in tables:
            return False

        columns_sql = ", ".join(columns)
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name}
        ({columns_sql})
        ENGINE = InnoDB
        """
        self.cursor.execute(query)
        Logs.log_change(f"Created table called {table_name}", user = "admin")

    def __connect(self, target_database, users = "admin"):
        try:
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=target_database
            )
            Logs.log_change(
                f"Successfully connected to database {target_database}",
                user = users
            )
            return True
        except mysql.connector.Error as err:
            print("MySQL error:", err)
            Logs.log_change(
                f"Failed to connect to database {target_database}",
                user = "admin"
            )
            raise ValueError(f"Unable to connect to {target_database}")
            return False


class UserManagement(Database):
    def __init__(self, aka = "system"):
        super().__init__("users", aka)
        self.__create_user_table()
        self.aka = aka

    def __create_user_table(self):
        cursor = self.cursor
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]

        if "users" in tables:
            return

        super()._create_table(
            "users",
            "id INT AUTO_INCREMENT PRIMARY KEY",
            "name VARCHAR(255) NOT NULL UNIQUE",
            "userpass VARCHAR(255) NOT NULL",
            "role VARCHAR(255) DEFAULT 'visitor'",
            "added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        )
        Logs.log_change("Created user table", user = "admin")

    def create_user(self, username, password, role="visitor"):
        roles = ["visitor", "admin", "test"]
        if role not in roles:
            raise Exception("Invalid role")
        value = (username, password, role)
        query = "INSERT INTO users (name, userpass, role) VALUES (%s,%s,%s)"
        self.cursor.execute(query, value)
        self.db.commit()
        Logs.log_change(
            f"Created new user {username} with role {role}",
            user="admin"
        )

    def delete_user(self, username, executer = "admin"):
        self.cursor.execute(f"DELETE FROM users WHERE name = '{username}'")
        self.db.commit()
        Logs.log_change(
            f"Deleted user {username}",
            user = executer
        )
        
        pass
    
    def get_users(self):
        self.cursor.execute("SELECT name, userpass, role FROM users")
        Logs.log_change("Requested all users", user = "admin")
        return self.cursor.fetchall()
    
    def validate_user_login(self, user, password):
        self.cursor.execute(f"SELECT name, userpass from users WHERE name = %s", (user,))
        detail = self.cursor.fetchone()
        if detail is None or detail[1] != password:
            return False
        else:
            return True

    def set_password(self, user, old_password, new_password):
        self.cursor.execute(f"SELECT name, userpass from users WHERE name = %s", (user,))
        detail = self.cursor.fetchone()
        if old_password != detail[1]:
            return False
        self.cursor.execute(f"UPDATE users SET userpass = %s WHERE name = %s", (new_password, user))
        self.db.commit()
        return True



if __name__ == "__main__": 
    Database().create_database("users")

