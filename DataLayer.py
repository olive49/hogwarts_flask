import os
import pathlib
from Human import Student
import json


class DataLayer:
    students_dict = {}

    def __init__(self):
        # self.students_dict = students_dict
        pass

    def get_student_by_email(self, student):
        if student is None:
            raise ValueError("Missing required student instance!")

        if student.get_email() in self.students_dict.keys():
            return student

    def set_student_by_email(self, student, student_email):
        if student is None:
            raise ValueError("Missing required student instance!")

        if not student.get_email() in self.students_dict.keys():
            self.students_dict[student_email] = student
            print(self)

    def get_all_students(self):
        for key, value in self.students_dict:
            print(key, value)
            return key, value

    def students_json_strings(self):
        students_strings = json.dumps(DataLayer.get_all_students(self))
        return students_strings

    def remove_student(self, student_email):
        try:
            del self.students_dict[student_email]
            return "Success"

        except Exception as e:
            raise Exception("something went wrong, error is: {}".format(e))


    @staticmethod
    def persist_students(student):
        try:
            DataLayer.students_dict[student.email] = student
            with open("Data/students.json", "w") as write_file:
                json.dump(DataLayer.students_dict, write_file, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
                return "Success"
        except Exception as e:
            raise Exception("something went wrong, error is: {}".format(e))

    @staticmethod
    def load_all_students(file):
        try:
            with open(file, "r") as read_file:
                if len(file) == 0:
                    pass
                else:
                    data = json.load(read_file)
                    print(data)
                    # DataLayer.students_dict.update(data)
                    # print("User dictionary", DataLayer.students_dict)
        except ValueError as e:
            print(e)

