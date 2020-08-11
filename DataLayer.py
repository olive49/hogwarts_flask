import os
import pathlib
from Human import Student
import datetime
import json
from MongoDaterLayer import MongoDataLayer


class DataLayer:
    mongoDB = MongoDataLayer()

    def __init__(self):
        self.students_dict = DataLayer.get_all_students()
        self.students_json_dict = DataLayer.load_all_students()
        self.admin_dict = {"veronica@hi.com": "hihihihi",
                           }

    @staticmethod
    def get_all_students():
        students = DataLayer.mongoDB.get_all_students()
        return students

    @staticmethod
    def add_student(student):
        new_student = DataLayer.mongoDB.add_student(student)
        return new_student

    @staticmethod
    def remove_student(student):
        DataLayer.mongoDB.remove_student(student)
        return True

    @staticmethod
    def edit_student(student, email):
        DataLayer.mongoDB.edit_student(student, email)
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
