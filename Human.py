import json

import datetime as datetime

from Validators import Validators
from datetime import datetime


class Human:
    def __init__(self, first_name, last_name, email, password):
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = password

    def get_email(self):
        return self._email


class Student(Human):
    def __init__(self, first_name, last_name, email, password, student_id, creation_time,
                 last_update, existing_magic_skills=[], desired_magic_skills=[]):
        super().__init__(first_name, last_name, email, password)
        self._id = student_id
        self.creation_time = creation_time
        self.last_update = last_update
        self.existing_magic_skills = existing_magic_skills
        self.desired_magic_skills = desired_magic_skills

    def __str__(self):
        existing_magic_skills = ''
        for skills in self.existing_magic_skills:
            existing_magic_skills += skills.__str__()
        if len(existing_magic_skills) == 0:
            existing_magic_skills = 'None'

        desired_magic_skills = ''
        for skills in self.desired_magic_skills:
            desired_magic_skills += skills.__str__()
        if len(desired_magic_skills) == 0:
            desired_magic_skills = 'None'

        self.last_update = str(datetime.now())

        student_json = json.dumps(self, default=lambda o: o.__dict__)
        return student_json

    def from_json(self, student_json):
        student_dict = json.loads(student_json)
        new_student = Student(student_dict["student_id"], student_dict["first_name"], student_dict["last_name"],
                              student_dict["email"], student_dict["password"], student_dict["creation_time"],
                              student_dict["last_update"], student_dict["existing_magic_skills"],
                              student_dict["desired_magic_skills"])
        return new_student

    def add_new_student(self, all_students_dict):
        Validators.all_required_fields(self)
        Validators.validate_name(self._first_name, self._last_name)
        Validators.validate_email(self._email)
        Validators.validate_password(self._password)
        Validators.validate_id(self._id)
        Validators.unique_email(self._email, all_students_dict)

    def edit_student(self, all_students_dict):
        Validators.all_required_fields(self)
        Validators.validate_name(self._first_name, self._last_name)
        Validators.validate_email(self._email)
        Validators.validate_password(self._password)
        Validators.validate_student_exists(self, all_students_dict)
        Validators.validate_id(self._id)

    def student_login(self):
        Validators.all_required_fields(self)
        Validators.validate_name(self._first_name, self._last_name)
        Validators.validate_email(self._email)
        Validators.validate_password(self._password)
        Validators.validate_id(self._id)

    def get_student_by_email(self):
        Validators.email_provided(self._email)
        Validators.validate_email(self._email)

    def get_added_students_per_date(self):
        pass


class Admin(Human):
    def __init__(self, first_name, last_name, email, password):
        super().__init__(first_name, last_name, email, password)


Becca = Student("Becca", "Teva", "teva@gmail.com", "Iloveicecream", 123453, 2020_03_06,
                2020_06_03, ["flying"], ["magic"])
