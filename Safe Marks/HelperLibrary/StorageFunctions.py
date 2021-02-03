import psycopg2
from psycopg2 import OperationalError


class StorageFunctions:
    def __init__(self, table_name, db_name="safe_marks", db_user="postgres", db_password="mt9j3f-D9eW.gfrV", db_host="127.0.0.1", db_port="5432"):
        self.connection = self._createconnection(db_name, db_user, db_password, db_host, db_port)
        self.table = table_name

    @staticmethod
    def _createconnection(db_name, db_user, db_password, db_host, db_port):
        connection = None
        try:
            connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        except OperationalError as error:
            print("The error", error, "occurred")
        return connection

    def _executequery(self, query, data, fetching=False):
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, data)
            if fetching:
                result = cursor.fetchall()
                return result
        except OperationalError as error:
            print("The error", error, "occurred")

    def append(self, list_of_values, data):
        data_records = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO " + self.table + f" " + list_of_values + f" VALUES ({data_records})"
        self._executequery(query, data, fetching=False)

    def list(self, item):
        query = f"SELECT " + item + f" FROM " + self.table
        data = self._executequery(query, data=None, fetching=True)
        data_list = []
        for data_item in data:
            data_list.append(data_item[0])
        return data_list

    def retrieve(self, column_list, data_list):
        query_condition = self.formquerycondition(column_list, data_list, False)
        query = f"SELECT * FROM " + self.table + " WHERE " + query_condition
        data_list = self._executequery(query, data=None, fetching=True)
        return list(data_list)

    def update(self, column_list, data_list, id, identifier="id"):
        query_condition = self.formquerycondition(column_list, data_list, True)
        query = f"UPDATE " + self.table + " SET " + query_condition + " WHERE " + identifier + " = " + str(id)
        self._executequery(query, data=None, fetching=False)

    @staticmethod
    def formquerycondition(column_list, data_list, updating=False):
        assert len(column_list) == len(data_list), "Columns list and data list do not match"
        query_condition = ""
        for counter in range(len(column_list)):
            query_condition = query_condition + column_list[counter] + " = '" + str(data_list[counter]) + "'"
            if updating:
                query_condition = query_condition + ", "
            else:
                query_condition = query_condition + " AND "
        if updating:
            query_condition = query_condition[:-2]
        else:
            query_condition = query_condition[:-5]
        return query_condition

    def delete(self, data, identifier="id"):
        query = f"DELETE FROM " + self.table + " WHERE " + identifier + " = " + str(data)
        self._executequery(query, data=None, fetching=False)
