import json
import datetime as datetime
from Validators import Validators
from datetime import datetime
import time
from typing import Dict, Optional
from Skill import Skill


class Human:
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def get_email(self):
        return self.email


class Student(Human):

    last_update = str(datetime.now())

    def __init__(self, student_id, first_name, last_name, email, password,
                 existing_magic_skills=[], desired_magic_skills=[]):
        super().__init__(first_name, last_name, email, password)

        existing_magic_skills_as_object = []
        for existing_skill_string in existing_magic_skills:
            existing_magic_skills_as_object.append(Skill(existing_skill_string))
            print(Skill(existing_skill_string))

        desired_magic_skills_as_object = []
        for desired_skill_string in desired_magic_skills:
            desired_magic_skills_as_object.append(Skill(desired_skill_string))
            print(Skill(desired_skill_string))

        self.id = student_id
        self.existing_magic_skills = existing_magic_skills_as_object
        self.desired_magic_skills = desired_magic_skills_as_object
        self.creation_time = str(datetime.now().date())
        # self.last_update = str(datetime.now())

    def __str__(self):
        local_student_dict = {self.email: {"first_name": self.first_name,
                                           "last_name": self.last_name,
                                           "email": self.email,
                                           "password": self.password,
                                           "existing_magic_skills": self.existing_magic_skills,
                                           "desired_magic_skills": self.desired_magic_skills
                                           }}
        string = "{}".format(local_student_dict)
        json.dumps(string, default=lambda o: o.__dict__)
        return string

    @staticmethod
    def add_existing_skill(student, skill):
        student["existing_magic_skills"].append(skill)
        last_update = str(datetime.now())
        student["last_update"] = last_update

        return student

    @staticmethod
    def add_desired_skills(student, skill):
        student["desired_magic_skills"].append(skill)
        last_update = str(datetime.now())
        student["last_update"] = last_update

        return student

    @staticmethod
    def from_json(student_json):
        student_dict = json.loads(student_json)
        new_student = Student(student_dict["student_id"], student_dict["first_name"], student_dict["last_name"],
                              student_dict["email"], student_dict["password"], student_dict["existing_magic_skills"],
                              student_dict["desired_magic_skills"])

        return new_student

    @staticmethod
    def add_new_student(student, students_dict):
        Validators.all_required_fields(student)
        Validators.validate_name(student['first_name'], student['last_name'])
        Validators.validate_email(student['email'])
        Validators.validate_password(student['password'])
        Validators.validate_id(student['student_id']) or Validators.validate_id('id')
        Validators.unique_email(student['email'], students_dict)
        return student, students_dict

    @staticmethod
    def edit_student(student, students_dict):
        Validators.all_required_fields(student)
        Validators.validate_name(student["first_name"], student["last_name"])
        Validators.validate_email(student["email"])
        Validators.validate_password(student["password"])
        Validators.validate_student_exists(student, students_dict)
        Validators.validate_id(student["id"]) or Validators.validate_id(student["student_id"])
        student["last_update"] = str(datetime.now())

    def student_login(self):
        Validators.all_required_fields(self)
        Validators.validate_name(self.first_name, self.last_name)
        Validators.validate_email(self.email)
        Validators.validate_password(self.password)
        Validators.validate_id(self.id)

    def get_student_by_email(self):
        Validators.email_provided(self.email)
        Validators.validate_email(self.email)


class Admin(Human):
    def __init__(self, first_name, last_name, email, password):
        super().__init__(first_name, last_name, email, password)

        # send a request so it knows this user is the admin
