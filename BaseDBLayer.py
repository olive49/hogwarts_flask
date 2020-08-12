
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

    def add_preson(self, person):
        pass

    def get_person_by_id(self, p_id):
        pass

    def insert_person(self, first_name, last_name, age, address):
        pass

    def get_all_persons(self):
        pass
