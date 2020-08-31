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
        self.__my_skill = {"Potion Making": 1, "Spells": 2, "Quidditch": 3,
                "Apparate": 4, "Metamorphmagi": 5, "Parseltongue": 6}

    def shutdown_db(self):
        self.__mydb.close()

    def get_all_students(self):
        try:
            self.__mydb.connect()
            cursor = self.__mydb.cursor()
            sql = "SELECT s.first_name, s.last_name, s.email, " \
                  "group_concat(DISTINCT es.skill_name, ':', " \
                  "concat(es.skill_rank) separator ',') as existing_skills, " \
                  "group_concat(DISTINCT ds.skill_name separator ',') as desired_skills " \
                  "FROM students s, existing_skills es, desired_skills ds " \
                  "WHERE s.id = es.student_id AND es.student_id = ds.student_id " \
                  "GROUP BY s.id;"
            cursor.execute(sql)
            res = cursor.fetchall()
            student_dict = []
            for f_name, l_name, email, e_skills, d_skills in res:
                existing_skills = []
                d = dict(x.split(":") for x in e_skills.split(","))
                for k,v in d.items():
                    e_skills_dict = {"Skill": k, "Level": v}
                    existing_skills.append(e_skills_dict)
                student = {"First_name": f_name, "Last_name": l_name, "Email": email,
                                "Existing_skills": existing_skills, "Desired_skills": d_skills}
                student_dict.append(student)
            print(type(student_dict), "student_dict")
            return student_dict

        except Error as error:
            print("Error reading data from MySQL table", error)

        # finally:
            # self.__mydb.close_connection()
            # cursor.close()

    def add_existing_skills(self, student, last_id):
        cursor = self.__mydb.cursor()
        for skill_name in student["existing_magic_skills"]:
            for skill, level in self.__my_skill.items():
                if skill_name["Skill"] == skill:
                    skill_id = level

            existing_skills = "INSERT INTO existing_skills (skill_id, skill_name, skill_rank, " \
                              "student_id) VALUES (%s, %s, %s, %s)"
            existing_val = (skill_id, skill_name["Skill"], skill_name["Level"], last_id)
            cursor.execute(existing_skills, existing_val)
        return

    def add_desired_skills(self, student, last_id):
        cursor = self.__mydb.cursor()
        for skill_name in student["desired_magic_skills"]:
            for skill, level in self.__my_skill.items():
                if skill_name["Skill"] == skill:
                    skill_id = level
            desired_skills = "INSERT INTO desired_skills (skill_id, skill_name, student_id) VALUES (%s, %s, %s)"
            desired_val = (skill_id, skill_name, last_id)
            cursor.execute(desired_skills, desired_val)
        return

    def add_student(self, student):
        try:
            self.__mydb._open_connection()
            self.__mydb.autocommit = False
            cursor = self.__mydb.cursor()
            # self.__mydb.start_transaction()
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
            if (self.__mydb.is_connected()):
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
            if (self.__mydb.is_connected()):
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
            self.__mydb.connect()
            cursor = self.__mydb.cursor()
            sql = "SELECT skill_name, COUNT(*) " \
                  "FROM desired_skills " \
                  "GROUP BY skill_name;"
            cursor.execute(sql)
            desired_list = []
            response = cursor.fetchall()
            for res, key in response:
                desired_list.append({'Skill': res, 'Count': key})
            return desired_list

        except Error as error:
            print("Error reading data from MySQL table", error)

        finally:
            if (self.__mydb.is_connected()):
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
            if (self.__mydb.is_connected()):
                cursor.close()
                self.__mydb.close()

    def update_existing_skills(self, data, student_id):
        cursor = self.__mydb.cursor()
        for skill_name in data["existing_magic_skills"]:
            for skill, level in self.__my_skill.items():
                if skill_name["Skill"] == skill:
                    skill_id = level
            existing_skills = "UPDATE existing_skills " \
                              "SET skill_id = %s, skill_name = %s, skill_rank = %s " \
                              "WHERE " \
                              "student_id = %s " \
                              "LIMIT 1"
            existing_val = (skill_id, skill_name["Skill"], skill_name["Level"], student_id)
            cursor.execute(existing_skills, existing_val)
        return

    def update_desired_skills(self, data, student_id):
        cursor = self.__mydb.cursor()
        for skill_name in data["desired_magic_skills"]:
            for skill, level in self.__my_skill.items():
                if skill_name["Skill"] == skill:
                    skill_id = level
            desired_skills = "UPDATE desired_skills " \
                             "SET skill_id = %s, skill_name = %s " \
                             "WHERE " \
                             "student_id = %s "
            desired_val = (skill_id, skill_name["Skill"], student_id)
            cursor.execute(desired_skills, desired_val)
        return

    def edit_student(self, data, student):
        try:
            self.__mydb._open_connection()
            cursor = self.__mydb.cursor()
            id_sql = "SELECT id " \
                     "FROM hogwarts.students " \
                     "WHERE email = %s;"
            cursor.execute(id_sql, (student,))
            student_id = cursor.fetchone()
            for id in student_id:
                print(id)
            self.__mydb.start_transaction()
            sql = "UPDATE students " \
                  "SET first_name = %s, last_name = %s, email = %s" \
                  "WHERE " \
                  "email = %s "
            student_data = (data["first_name"], data["last_name"], data["email"], student)
            cursor.execute(sql, student_data)
            MySqlDataLayer.update_existing_skills(self, data, id)
            MySqlDataLayer.update_desired_skills(self, data, id)
            self.__mydb.commit()
            print(cursor.rowcount, "record updated.")
            return cursor.rowcount

        except Error as error:
            print("Failed to update record to database rollback: {}".format(error))
            self.__mydb.rollback()

        finally:
            if (self.__mydb.is_connected()):
                cursor.close()
                self.__mydb.close()
