import mysql.connector
from mysql.connector import errorcode
import GUI.backend.tables as Tables


class Database:
    def __init__(self, host, user, password, db_name='industry4', pool_name='mypool'):
        self.db_name = db_name
        self.host = host
        self.password = password
        self.user = user
        self.pool_name = pool_name

    def __exit__(self, a, s, d):
        print(a,s,d)
        self.cursor.execute("DROP DATABASE industry4")
        self.connection.close()

    def dropDB(self):
        self.cursor.execute("DROP DATABASE industry4")

    def connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.host, user=self.user, pool_name=self.pool_name, password=self.password, pool_size=8)
            self.cursor = self.connection.cursor(buffered=True)
            if self.db_name is not None:
                self.cursor.execute(f'USE {self.db_name}')
                print("Connection Established.")
            return 0
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the username or password")
                return -1
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                self.cursor.execute(f'CREATE DATABASE {self.db_name}')
                print(f'Database {self.db_name} created')
                self.cursor.execute(f'USE {self.db_name}')
                return 1
            else:
                print(err)
                return -1

    def create_tables(self, tables: dict):
        for table_name in tables:
            tables_description = tables[table_name]
            print(tables_description)
            try:
                print("Creating table{}: ".format(table_name), end='')
                self.cursor.execute(tables_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print('already exists.')
                else:
                    print(err.msg)
            else:
                print("OK")

    def getTables(self):
        try:
            self.cursor.execute('SHOW TABLES')
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)



    def insert_into(self, table: str, fields: str, data: tuple, conditions: str=None, extra: str=None):
        """
        INSERT INTO {table}({fields}) VALUES (data_tuple) WHERE {conditions} {extra}
        Builds a string query for sql based on length of data tuple and executes
        Args:
            fields (dict): Dictionary containing string name of column for key and value being values to add to db
        """

        # Create the correct number of '%s' for the SQL query and concat to string, removing ' from the %s
        v = tuple(('%s' for i in range(len(data))))
        values = "VALUES " + str(v).replace("'","")

        query = f"INSERT INTO {table}({fields}) " + values
        if conditions:
            query += f"WHERE {conditions}"
        if extra:
            query += f" {extra}"
        try:
            self.cursor.execute(query, data)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(err)

    def selection(self, table: str, columns: str, conditions: str=None, extra: str=None):
        temp = f'SELECT {columns} FROM {table}'
        if conditions:
            temp += f' WHERE {conditions}'
        if extra:
            temp += f' {extra}'

        try:
            self.cursor.execute(temp)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)


    def showColumns(self, table:str):
        try:
            self.cursor.execute(f'SHOW COLUMNS FROM {table}')
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)

    def updateTable(self, table: str, fields: tuple, data: tuple, condition: str=None):
        """
        UPDATE {table_name} SET {field[i]} = {data[i]} WHERE {condition}
        """
        temp = f'UPDATE {table} SET '
        temp += fields + " = " + data + ' '
        
        if condition:
            temp += f'WHERE {condition}'
        try:
            self.cursor.execute(temp)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(err)

