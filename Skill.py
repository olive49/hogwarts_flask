import json


class Skill:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        skill_name = json.dumps(self, default=lambda o: o.__dict__)
        return skill_name
