
class BaseDBLayer:

    def __init__(self):
        pass

    def signup(self, name, email, password):
        pass

    def login(self, email, password):
        pass

    def __connect(self):
        pass

    def shutdown(self):
        pass

    def add_student(self, student):
        pass

    def get_student_by_id(self, s_id):
        pass

    def insert_student(self, first_name, last_name, email, existing_skills, desired_skills, creation_time, last_update):
        pass

    def get_all_students(self):
        pass
