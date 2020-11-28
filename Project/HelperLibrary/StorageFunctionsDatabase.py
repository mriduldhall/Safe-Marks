import psycopg2
from psycopg2 import OperationalError


class StorageFunctions:
    def __init__(self, table_name, data, db_name="safe_marks", db_user="postgres", db_password="mt9j3f-D9eW.gfrV", db_host="127.0.0.1", db_port="5432"):
        self.connection = self._createconnection(db_name, db_user, db_password, db_host, db_port)
        self.table = table_name
        self.data = data

    @staticmethod
    def _createconnection(db_name, db_user, db_password, db_host, db_port):
        connection = None
        try:
            connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        except OperationalError as error:
            print("The error", error, "occurred")
        return connection

    def executequery(self, query, fetching=False):
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, self.data)
            if fetching:
                result = cursor.fetchall()
                return result[0]
        except OperationalError as error:
            print("The error", error, "occurred")

    def append(self):
        data_records = ", ".join(["%s"] * len(self.data))
        query = f"INSERT INTO " + self.table + f" (username, password) VALUES {data_records}"
        self.executequery(query, fetching=False)

    def list(self, item):
        query = f"SELECT " + item + f" FROM " + self.table
        data = self.executequery(query, fetching=True)
        return list(data)

    def retrieve(self, item):
        query = f"SELECT * FROM " + self.table + " WHERE " + item + f" = '" + self.data + "'"
        data = self.executequery(query, fetching=True)
        return list(data)

    def update(self, item, id, identifier="id"):
        query = f"UPDATE " + self.table + " SET " + item + " = '" + self.data + "' WHERE " + identifier + " = " + id
        self.executequery(query, fetching=False)

    def delete(self, id, identifier="id"):
        query = f"DELETE FROM " + self.table + " WHERE " + identifier + " = " + str(id)
        self.executequery(query, fetching=False)


if __name__ == '__main__':
    # create_test_table = """CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL)"""
    # StorageFunctions("test2", None).executequery(create_test_table)

    # APPEND TEST CASE
    # username = input("Enter a username:")
    # password = input("Enter a password:")
    # user_data = [(username, password)]
    # StorageFunctions("test", user_data).append()

    # LIST TEST CASE
    # data = StorageFunctions("test", None).list("username")
    # print(data)

    # RETRIEVE TEST CASE
    # data = StorageFunctions("test", "admin").retrieve("username")
    # print(data)

    # UPDATE TEST CASE
    # StorageFunctions("test", "test").update("username", "7")

    # DELETE TEST CASE
    # username = input("Enter a username:")
    # data = StorageFunctions("test", username).retrieve("username")
    # id = data[0]
    # StorageFunctions("test", None).delete(id)

    pass
