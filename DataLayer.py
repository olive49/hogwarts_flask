import os
import pathlib
from Human import Student
import datetime
import json
from MongoDaterLayer import MongoDataLayer
from MySqlDataLayer import MySqlDataLayer
from decouple import config


class DataLayer:
    if config("DB") == "Mysql":
        data_layer = MySqlDataLayer()
    else:
        data_layer = MongoDataLayer()


    def __init__(self):
        # self.students_dict = DataLayer.get_all_students()
        # self.desired_skills_dict = DataLayer.get_desired_skills_count()
        # self.existing_skills_dict = DataLayer.get_existing_skills_count()
        self.admin_dict = {"veronica@hi.com": "hihihihi",
                           }

    @staticmethod
    def shutdown():
        DataLayer.data_layer.shutdown()

    @staticmethod
    def get_all_students():
        students = DataLayer.data_layer.get_all_students()
        return students

    @staticmethod
    def get_desired_skills_count():
        desired_skills = DataLayer.data_layer.get_desired_skills_count()
        return desired_skills

    @staticmethod
    def get_existing_skills_count():
        # desired_skills = DataLayer.data_layer.get_existing_skills_count()
        # return desired_skills
        return

    @staticmethod
    def add_student(student):
        new_student = DataLayer.data_layer.add_student(student)
        return new_student

    @staticmethod
    def remove_student(student):
        DataLayer.data_layer.remove_student(student)
        return True

    @staticmethod
    def remove_all_students():
        DataLayer.data_layer.remove_all_students()

    @staticmethod
    def edit_student(student, email):
        DataLayer.data_layer.edit_student(student, email)
        return True

    def set_student_by_email(self, student):
        if student is None:
            raise ValueError("Missing required student instance!")

        if not student.get_email() in self.students_dict:
            return

    def is_admin(self, admin):
        if admin['admin_email'] in self.admin_dict:
            return True
        return False

    def get_student_by_email(self, email):
        print(self.students_dict)
        if email is None:
            raise ValueError("Missing required student instance!")

        if email not in self.students_dict:
            raise ValueError("Missing required student instance in dictionary!")

        if email in self.students_dict:
            dict_value = self.students_dict.get(email)
            return json.dumps(dict_value)

    def get_students_by_add_date(self, creation_time):
        dates = []

        for key in self.students_dict:
            if self.students_dict[key]['creation_time'].startswith(creation_time):
                dates.append(key)
                print(self.students_dict[key]['creation_time'])
            else:
                return "no students added"
        return json.dumps(dates)

    def get_students_by_existing_skills(self, requested_skill):
        students_with_matching_skill = []

        for student_key in self.students_dict:
            student_skills = self.students_dict[student_key]['existing_magic_skills'][0].split(',')
            for student_skill in student_skills:
                if requested_skill in student_skill:
                    students_with_matching_skill.append(student_key)
        if len(students_with_matching_skill) > 0:
            return json.dumps(students_with_matching_skill)
        else:
            return "no students with existing skill"

    def get_students_by_desired_skills(self, desired_skill):
        students_with_desired_skill = []

        lc_desired_skill = desired_skill.lower()
        for student_key in self.students_dict:
            student_skills = self.students_dict[student_key]['desired_magic_skills'][0].split(',')
            for student_skill in student_skills:
                if lc_desired_skill in student_skill:
                    students_with_desired_skill.append(student_key)
        if len(students_with_desired_skill) > 0:
            return json.dumps(students_with_desired_skill)
        else:
            return "no students with desired skill"

    def students_json_strings(self):
        students_strings = json.dumps(DataLayer.get_all_students(self))
        return students_strings

    @staticmethod
    def load_all_students():
        try:
            with open("Data/students.json", "r") as read_file:
                if len("Data/students.json") == 0:
                    pass
                else:
                    data = json.load(read_file)
                    return data
        except ValueError as e:
            print(e)


    # def remove_student(self, student_email):
    #     try:
    #         print("The dictionary before performing remove is : " + str(self.students_dict))
    #         del self.students_dict[student_email]
    #         print("The dictionary after remove is : " + str(self.students_dict))
    #
    #     except Exception as e:
    #         raise Exception("something went wrong, error is: {}".format(e))

    # def persist_students(self):
    #     try:
    #         with open("Data/students.json", "w") as write_file:
    #             json.dump(self.students_dict, write_file, default=lambda obj: obj.__dict__, sort_keys=True,
    #                       indent=4)
    #             return "Success"
    #     except Exception as e:
    #         raise Exception("something went wrong, error is: {}".format(e))
