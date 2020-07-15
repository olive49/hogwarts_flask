import os
import pathlib
from Human import Student
import json


class DataLayer:
    students_dict = {}

    def __init__(self, students_dict):
        self.students_dict = students_dict

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

    def persist_students(self):
        try:
            with open("students.json", "w") as write_file:
                json.dump(self.students_dict, write_file, default=lambda obj: obj.__dict__, sort_keys=True, indent=2)
                return "Success"
        except ValueError as e:
            print(e)


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
                    DataLayer.students_dict.update(data)
                    print("User dictionary", DataLayer.students_dict)
        except ValueError as e:
            print(e)

        #     folder_where_json_file_is = pathlib.Path(__file__).parent
        #     read_file = str(folder_where_json_file_is) + os.path.join("students.json")
        #
        #     if os.path.exists(read_file):
        #         with open("students.json", "r") as f:
        #             json_content = json.load(f)
        #             students_dict = {json_content.email: json_content.__str__()}
        #
        #         return students_dict
        #     else:
        #         raise Exception("File doesn't exist")
        #     return "Success"
        #
        # except Exception as e:
        #     raise Exception("something went wrong, error is: {}".format(e))
