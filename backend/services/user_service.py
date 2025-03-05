from fastapi import HTTPException
from datetime import datetime

def validate_email(email: str):
    if any(
        [
            " " in email,
            "@" not in email,
            "." not in email,
            email.count("@") != 1,
        ]
    ):
        return False
    return True

def validate_password(password: str):
    if any(
        [
            len(password) < 8,
            not any(char.isupper() for char in password),
            not any(char.islower() for char in password),
            not any(char.isdigit() for char in password),
        ]
    ):
        return False
    return True

def validate_name(name: str):
    if any(
        [
            " " in name,
            len(name) < 2,
            len(name) > 50,
        ]
    ):
        return False
    return True


class UserCreate:
    def __init__(self, email: str, password: str, name: str):
        if not all(
            [
                validate_email(email),
                validate_password(password),
                validate_name(name),
            ]
        ):
            raise HTTPException(status_code=406, detail="Invalid email, password, or name")

        self.email = email
        self.password = password
        self.name = name

