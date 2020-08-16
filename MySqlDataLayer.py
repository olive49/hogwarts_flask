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

    def add_existing_skills(self, student):
        cursor = self.__mydb.cursor()
        existing_list = []
        for skill in student["existing_magic_skills"]:
            existing_skills = "INSERT INTO existing_skills (skill_name, skill_rank) VALUES (%s, %s)"
            existing_val = (skill["Skill"], skill["Level"])
            cursor.execute(existing_skills, existing_val)
            self.__mydb.commit()
            existing_last = cursor.lastrowid
            existing_list.append(existing_last)
        return existing_list

    def add_desired_skills(self, student):
        cursor = self.__mydb.cursor()
        desired_list = []
        for skill in student["desired_magic_skills"]:
            print("skill desire loop", skill)
            desired_skills = "INSERT INTO desired_skills (skill_name) VALUES (%s)"
            cursor.execute(desired_skills, (skill,))
            self.__mydb.commit()
            desired_last = cursor.lastrowid
            desired_list.append(desired_last)
        return desired_list


    def add_student(self, student):
        try:
            cursor = self.__mydb.cursor()
            sql = "INSERT INTO students (first_name, last_name, email, created_at, " \
                  "last_update) VALUES (%s, %s, %s, %s, %s)"
            val = (student["first_name"], student["last_name"], student["email"],
                   student["creation_time"], student["last_update"])
            cursor.execute(sql, val)
            last_id = cursor.lastrowid
            existing = MySqlDataLayer.add_existing_skills(self, student)
            desired = MySqlDataLayer.add_desired_skills(self, student)
            for exist in existing:
                for desire in desired:
                    magic_skills = "INSERT INTO magic_skills (student_id, existing_skill_id, " \
                           "desired_skill_id) VALUES (%s, %s, %s)"
                    magic_val = (last_id, exist, desire)
                    cursor.execute(magic_skills, magic_val)
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


    def remove_all_students(self):
        try:
            cursor = self.__mydb.cursor()
            sql = "DELETE FROM students"
            cursor.execute(sql)
            self.__mydb.commit()
            print("all student records removed")
            return

        except Error as error:
            print("Failed to remove student records: {}".format(error))

        finally:
            cursor.close()





