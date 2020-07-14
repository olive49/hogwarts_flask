from Human import Student
import json

class DataLayer:
    def __init__(self, students_dict={}):
        self._students_dict = students_dict

    def get_student_by_email(self, student):
        if student is None:
            raise ValueError("Missing required student instance!")

        if student.get_email() in self._students_dict.keys():
            return student

    def set_student_by_email(self, student, student_email):
        if student is None:
            raise ValueError("Missing required student instance!")

        if not student.get_email() in self._students_dict.keys():
            self._students_dict[student_email] = student
            print(self)

    def get_all_students(self):
        for key, value in self._students_dict:
            print(key, value)
            return key, value

    def students_json_strings(self):
        students_strings = json.dumps(DataLayer.get_all_students(self))
        return students_strings

    def remove_student(self, student_email):
        if student_email not in self._students_dict.keys():
            raise ValueError("Student email does not exist")

        student = self._students_dict[student_email]
        for key in self._students_dict:
            if student_email == key:






















