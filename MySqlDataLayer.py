import mysql.connector
from mysql.connector import Error
from BaseDBLayer import BaseDBLayer

from decouple import config

class MySqlDataLayer(BaseDBLayer):
    def __init__(self):
        super().__init__()
        self.__connect()

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
            sql = "SELECT first_name, last_name, email FROM students"
            cursor.execute(sql)
            res = cursor.fetchall()
            return res

        except Error as error:
            print("Error reading data from MySQL table", error)

        finally:
            cursor.close()

    def add_student(self, student):
        try:
            cursor = self.__mydb.cursor()
            for skill in student["existing_magic_skills"]:
                print(skill)
            for skill_name in student["desired_magic_skills"]:
                print(skill_name)
            sql = "INSERT INTO students (first_name, last_name, email, created_at, " \
                  "last_update) VALUES (%s, %s, %s, %s, %s)"
            val = (student["first_name"], student["last_name"], student["email"],
                   student["creation_time"], student["last_update"])
            cursor.execute(sql, val)
            existing_skills = "INSERT INTO existing_skills (skill_name, skill_rank) VALUES (%s, %s)"
            existing_val = (skill["Skill"], skill["Level"])
            desired_skills = "INSERT INTO desired_skills (skill_name) VALUES (%s)"
            desired_val = (student["desired_magic_skills"])
            last_id = cursor.lastrowid
            cursor.execute(existing_skills, existing_val, last_id)
            cursor.execute(desired_skills, desired_val, last_id)
            self.__mydb.commit()
            print(cursor.rowcount, "record inserted.")
            return cursor.rowcount

        except Error as error:
            print("Failed to update record to database rollback: {}".format(error))

        finally:
            cursor.close()


    def remove_student(self, student):
        try:
            cursor = self.__mydb.cursor()
            sql = "DELETE FROM students WHERE email = %s"
            cursor.execute(sql, (student,))
            self.__mydb.commit()
            print("record removed")
            return

        except Error as error:
            print("Failed to remove student: {}".format(error))

        finally:
            cursor.close()



