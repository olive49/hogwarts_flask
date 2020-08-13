import mysql.connector
from mysql.connector import Error
from BaseDBLayer import BaseDBLayer

from decouple import config


class MySqlDataLayer(BaseDBLayer):
    def __init__(self):
        super().__init__()
        self.__connect()
        self.__mydb.autocommit = True

    def __connect(self):
        self.__mydb = mysql.connector.connect(
            host="localhost",
            user=config('MYSQL_USER'),
            password=config('PASSWORD'),
            database="hogwarts"
        )

    def shutdown_db(self):
        self.__mydb.close()

    def get_all_students(self):
        try:
            cursor = self.__mydb.cursor()
            print(cursor)
        #     sql = "SELECT first_name,last_name,age,address FROM persons WHERE id=%s"
        #     cursor.execute(sql)
        #     res = cursor.fetchone()
        #     return res
        finally:
            cursor.close()

    def add_student(self, student):
        try:
            cursor = self.__mydb.cursor()
            sql = "INSERT INTO students (first_name, last_name, email, created_at, " \
                  "last_update) VALUES (%s, %s, %s, %s, %s)"
            val = (student["first_name"], student["last_name"], student["email"],
                   student["creation_time"], student["last_update"])
            cursor.execute(sql, val)
            print(cursor.rowcount, "record inserted.")
            return cursor.rowcount

        except mysql.connector.Error as error:
            print("Failed to update record to database rollback: {}".format(error))
        #
        finally:
            cursor.close()
