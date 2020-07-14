class Validators:
    def __init__(self, student):
        self.student = student

    @staticmethod
    def all_required_fields(student):
        if student["first_name"] is None:
            raise Exception("first_name is missing")
        if student["last_name"] is None:
            raise Exception("last_name is missing")
        if student["email"] is None:
            raise Exception("email is missing")
        if student["password"] is None:
            raise Exception("password is missing")
        if student["student_id"] is None:
            raise Exception("password2 is missing")
        if student["creation_time"] is None:
            raise Exception("creation_time is missing")
        if student["last_update"] is None:
            raise Exception("last_update is missing")
        if student["existing_magic_skills"] is None:
            raise Exception("existing_magic_skills is missing")
        if student["desired_magic_skills"] is None:
            raise Exception("desired_magic_skills is missing")

    @staticmethod
    def validate_name(first_name, last_name):
        invalid_chars = ["*", "<", ">", "!", "@", "#", "$", "%", "^", "&"]
        for char in invalid_chars:
            if char in first_name:
                raise Exception("Your first name contains an invalid character")
            if char in last_name:
                raise Exception("Your last name contains an invalid character")
        return True

    @staticmethod
    def validate_email(email):
        if not "@" in email:
            raise Exception("Your email is invalid because it is missing an @")
        if not ".com" in email:
            raise Exception("Your email is invalid because it is missing .com")
        else:
            return True

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise Exception("Your password needs to be at least 8 characters")
        if password.isalnum() is False:
            raise Exception("Your password can only have alphanumeric characters")

    @staticmethod
    def validate_id(student_id):
        if len(student_id) < 6:
            raise Exception("Student ID is not valid - must be at least 6 characters")
        if student_id.isinstance() is False:
            raise Exception("Student ID must be numbers only")

    @staticmethod
    def validate_student_exists(student, all_students):
        if student["email"] in all_students:
            return True
        else:
            raise Exception("Student doesn't exist")


