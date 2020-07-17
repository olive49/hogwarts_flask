import os
import pathlib
from Human import Student
import datetime
import json


class DataLayer:

    def __init__(self, students_dict={}):
        self.students_dict = DataLayer.load_all_students()

    def get_student_by_email(self, email):
        print(self.students_dict)
        if email is None:
            raise ValueError("Missing required student instance!")

        if email not in self.students_dict:
            raise ValueError("Missing required student instance in dictionary!")

        if email in self.students_dict:
            dict_value = self.students_dict.get(email)
            return dict_value

    def set_student_by_email(self, student, student_email):
        if student is None:
            raise ValueError("Missing required student instance!")

        if not student.get_email() in self.students_dict.keys():
            self.students_dict[student_email] = student
            print(self.students_dict)

    def get_all_students(self):
        for key, value in self.students_dict:
            print(key, value)
            return key, value

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
            return "no students with this skill"

    def students_json_strings(self):
        students_strings = json.dumps(DataLayer.get_all_students(self))
        return students_strings

    def remove_student(self, student_email):
        try:
            del self.students_dict[student_email]
            return "Success"

        except Exception as e:
            raise Exception("something went wrong, error is: {}".format(e))

    def persist_students(self, student):
        try:
            # self.students_dict[student.email] = student
            with open("Data/students.json", "w") as write_file:
                json.dump(self.students_dict, write_file, default=lambda obj: obj.__dict__, sort_keys=True,
                          indent=4)
                return "Success"
        except Exception as e:
            raise Exception("something went wrong, error is: {}".format(e))

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
