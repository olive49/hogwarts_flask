import mysql.connector

from decouple import config
from BaseDBLayer import BaseDBLayer

class MySqlDataLayer(BaseDBLayer):

    def get_person_by_id(self, id):
        try:
            cursor = self.__mydb.cursor()
            sql = "SELECT first_name, last_name"

