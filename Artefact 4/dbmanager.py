import datetime
import mysql.connector
from cryptography.fernet import Fernet


k = open("key.txt", "r")


def log_change(change, user = "admin"):
    logs = open("log.txt", "a")
    now = datetime.datetime.today().replace(microsecond=0)
    logs.write(f"{user}: {change}: {now}\n")
    logs.close()


class Database:
    def __init__(self, target_database):
        self.host = "localhost"
        self.user = "root"
        self.password = "C0ventryCUC"
        self.cursor = None
        self.db = None

        if not self.__connect(target_database):
            print(f"failed to connect to {target_database}")
            return
        else:
            self.cursor = self.db.cursor()
            print(f"successfuly connected to {target_database}")
            log_change("Connected to database", user = "admin")
            # test
            # self.__create_database("johnCena")

    def _create_database(self, name):
        cursor = self.cursor
        cursor.execute("SHOW DATABASES")
        if name not in cursor:
            try:
                cursor.execute(f"CREATE DATABASE {name}")
                log_change(f"Created database called {name}", user = "admin")
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
        log_change(f"Created table called {table_name}", user = "admin")

    def __connect(self, target_database):
        try:
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=target_database
            )
            log_change(
                f"Successfully connected to database {target_database}",
                user = "admin"
            )
            return True
        except mysql.connector.Error as err:
            print("MySQL error:", err)
            log_change(
                f"Failed to connect to database {target_database}",
                user = "admin"
            )
            return False


class UserManagement(Database):
    def __init__(self):
        super().__init__("users")
        self.__create_user_table()

    def __create_user_table(self):
        cursor = self.cursor
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]

        if "users" in tables:
            return

        super()._create_table(
            "users",
            "name CHAR(255) NOT NULL",
            "userpass TEXT(255) NOT NULL",
            "role CHAR(255) DEFAULT 'visitor'",
            "added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        )
        log_change("Created user table", user = "admin")

    def create_user(self, username, password, role="visitor", fernet=None):
        roles = ["visitor", "admin", "test"]
        if role not in roles:
            raise Exception("Invalid role")

        if fernet is None:
            key = k.readline().strip().encode("utf-8")
            fernet = Fernet(key)

        token = fernet.encrypt(password.encode("utf-8"))

        value = (username, token, role)
        query = "INSERT INTO users (name, userpass, role) VALUES (%s,%s,%s)"
        self.cursor.execute(query, value)
        self.db.commit()
        log_change(
            f"Created new user {username} with role {role}",
            user="admin"
        )
        # print(token)
        # print(fernet.decrypt(token))
        # print(str(fernet.decrypt(token))[2:-1])

    def delete_user(self, username, executer = "admin"):
        self.cursor.execute(f"DELETE FROM users WHERE name = '{username}'")
        self.db.commit()
        log_change(
            f"Deleted user {username}",
            user = executer
        )
        
        pass

    def set_password(self, old_password, new_password):
        pass

    def get_user(self, user):
        pass


db = UserManagement()
cursor = db.cursor
for i in range(10):
    db.delete_user("test")

k.close()


