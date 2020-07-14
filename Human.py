class Human:
    def __init__(self, first_name, last_name, email, password):
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = password


class Student(Human):
    def __init__(self, first_name, last_name, email, password, student_id, creation_time,
                 last_update, existing_magic_skills, desired_magic_skills):
        super().__init__(first_name, last_name, email, password)
        self._id = student_id
        self.creation_time = creation_time
        self.last_update = last_update
        self.existing_magic_skills = existing_magic_skills
        self.desired_magic_skills = desired_magic_skills

    def __str__(self):
        return '"Student ID": {},\n"First Name": {},\n"Last Name": {},\n"Email": {}\n"Password": {}' \
               '\n"Creation Time": {}, \n"Last Update": {}, \n"Existing Magic Skills": {}, ' \
               '\n"Desired Magic Skills": {} '.format(self._id, self._first_name, self._last_name, self._email,
                                                      self._password, self.creation_time, self.last_update,
                                                      self.existing_magic_skills, self.desired_magic_skills)


class Admin(Human):
    def __init__(self, first_name, last_name, email, password):
        super().__init__(first_name, last_name, email, password)