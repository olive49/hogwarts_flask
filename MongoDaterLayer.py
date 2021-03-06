import pymongo
from BaseDBLayer import BaseDBLayer


class MongoDataLayer(BaseDBLayer):

    def __init__(self):
        super().__init__()
        self.__connect()

    def __connect(self):
        self.__client = pymongo.MongoClient('localhost', 27017)
        self.__db = self.__client["hogwarts_db"]

    def shutdown(self):
        self.__client.close()

    def get_all_students(self):
        student_list = []
        for student in self.__db["students"].find():
            del student["_id"]
            student_list.append(student)
        return student_list

    def get_desired_skills_count(self):
        pipeline = [{"$group": {"_id": "$desired_magic_skills", "myCount": {"$sum": 1}}}]
        val = list(self.__db["students"].aggregate(pipeline))
        return val

    def get_existing_skills_count(self):
        pipeline = [{"$unwind": "$existing_magic_skills"}, {"$group": {"skills": "skills"},
                                                            "myCount": {"$sum": 1}}]
        val = list(self.__db["students"].aggregate(pipeline))
        return val

    def add_student(self, student):
        self.__db["students"].insert(student)
        return True

    def remove_student(self, student_email):
        self.__db["students"].remove({"email": student_email})
        return

    def edit_student(self, student, email):
        self.__db["students"].update({"email": email}, student)
        return
