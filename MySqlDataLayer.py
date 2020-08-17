import mysql.connector
from flask import jsonify
from mysql.connector import Error
from BaseDBLayer import BaseDBLayer
import json

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

    def add_existing_skills(self, student, last_id):
        cursor = self.__mydb.cursor()
        for skill in student["existing_magic_skills"]:
            if skill["Skill"] == "Potion Making":
                skill_id = 1
            elif skill["Skill"] == "Spells":
                skill_id = 2
            elif skill["Skill"] == "Quidditch":
                skill_id = 3
            elif skill["Skill"] == "Apparate":
                skill_id = 4
            elif skill["Skill"] == "Metamorphmagi":
                skill_id = 5
            elif skill["Skill"] == "Parseltongue":
                skill_id = 6
            existing_skills = "INSERT INTO existing_skills (skill_id, skill_name, skill_rank, " \
                              "student_id) VALUES (%s, %s, %s, %s)"
            existing_val = (skill_id, skill["Skill"], skill["Level"], last_id)
            cursor.execute(existing_skills, existing_val)
        return

    def add_desired_skills(self, student, last_id):
        cursor = self.__mydb.cursor()
        for skill in student["desired_magic_skills"]:
            if skill == "Potion Making":
                skill_id = 1
            elif skill == "Spells":
                skill_id = 2
            elif skill == "Quidditch":
                skill_id = 3
            elif skill == "Apparate":
                skill_id = 4
            elif skill == "Metamorphmagi":
                skill_id = 5
            elif skill == "Parseltongue":
                skill_id = 6
            print("skill desire loop", skill)
            desired_skills = "INSERT INTO desired_skills (skill_id, skill_name, student_id) VALUES (%s, %s, %s)"
            desired_val = (skill_id, skill, last_id)
            cursor.execute(desired_skills, desired_val)
        return


    def add_student(self, student):
        try:
            self.__mydb._open_connection()
            self.__mydb.autocommit = False
            cursor = self.__mydb.cursor()
            self.__mydb.start_transaction()
            sql = "INSERT INTO students (first_name, last_name, email, created_at, " \
                  "last_update) VALUES (%s, %s, %s, %s, %s)"
            val = (student["first_name"], student["last_name"], student["email"],
                   student["creation_time"], student["last_update"])
            cursor.execute(sql, val)
            last_id = cursor.lastrowid
            MySqlDataLayer.add_existing_skills(self, student, last_id)
            MySqlDataLayer.add_desired_skills(self, student, last_id)
            self.__mydb.commit()
            print(cursor.rowcount, "record inserted.")
            return cursor.rowcount

        except Error as error:
            print("Failed to update record to database rollback: {}".format(error))
            self.__mydb.rollback()

        finally:
            if(self.__mydb.is_connected()):
                cursor.close()
                self.__mydb.close()


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
            self.__mydb.rollback()

        finally:
            if(self.__mydb.is_connected()):
                cursor.close()
                self.__mydb.close()


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


    def get_desired_skills_count(self):
        try:
            self.__mydb._open_connection()
            cursor = self.__mydb.cursor()
            sql = "SELECT skill_name, COUNT(*) " \
                  "FROM desired_skills " \
                  "GROUP BY skill_name;"
            cursor.execute(sql)
            desired_list = []
            response = cursor.fetchall()
            for res, key in response:
                desired_list.append({'Skill': res, 'Count': key})
            return json.dumps(desired_list)

        except Error as error:
            print("Error reading data from MySQL table", error)

        finally:
            if(self.__mydb.is_connected()):
                cursor.close()
                self.__mydb.close()


    def get_existing_skills_count(self):
        try:
            self.__mydb._open_connection()
            cursor = self.__mydb.cursor()
            sql = "SELECT skill_name, COUNT(*) " \
                  "FROM existing_skills " \
                  "GROUP BY skill_name;"
            cursor.execute(sql)
            existing_list = []
            response = cursor.fetchall()
            for res, key in response:
                existing_list.append({'Skill': res, 'Count': key})
            return json.dumps(existing_list)

        except Error as error:
            print("Error reading data from MySQL table", error)

        finally:
            if(self.__mydb.is_connected()):
                cursor.close()
                self.__mydb.close()





