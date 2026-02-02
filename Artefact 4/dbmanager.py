import mysql.connector

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
            #test
            #self.__create_database("johnCena")
            
    def __create_database(self, name):
        cursor = self.cursor
        cursor.execute("SHOW DATABASES")
        if name not in cursor:
            try:
                cursor.execute(f"CREATE DATABASE {name}")
            except:
                print(f"database '{name}' could not be created")
            
    def __create_table(self, table_name, *columns):
        cursor = self.cursor
        columns_sql = ", ".join(columns)
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name}
        ({columns_sql})
        ENGINE = InnoDB
        """
        self.cursor.execute(query)
        
    def __connect(self, target_database):
        try:
            self.db = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = target_database
            )
            return True
        except mysql.connector.Error as err:
            print("MySQL error:", err)
            return False
            
        
class UserManagement(Database):
    def __init__(self):
        super().__init__("users")
        

        

        

        

db = UserManagement()
cursor = db.cursor
cursor.execute("SHOW DATABASES")



