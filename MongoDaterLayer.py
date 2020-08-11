import pymongo

class MongoDataLayer:

    def __create(self):
        self.__client = pymongo.MongoClient('localhost', 27017)
        self.__db = self.__client["hogwarts_db"]

    def __init__(self):
        self.__create()

    def shutdown(self):
        self.__client.close()

    def get_all_students(self):
        student_list = []
        for student in self.__db["students"].find():
            del student["_id"]
            student_list.append(student)
        return student_list

    def add_student(self, student):
        self.__db["students"].insert(student)
        return True

    def remove_student(self, student_email):
        self.__db["students"].remove({"email": student_email})
        return

    def edit_student(self, student, email):
        self.__db["students"].update({"email": email}, student)
        return
