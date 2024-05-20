from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import bcrypt
import re
from email_validator import validate_email, EmailNotValidError


class Id(BaseModel):
    id: str


class New_user(BaseModel):
    username: str = Field(max_length=50)
    password: str
    email: str
    books_in_library: List[str]

    @field_validator("password")
    def password_validate(cls, password: str):
        if len(password) < 8:
            raise ValueError('Пароль должен состоять как минимум из 8 символов')
        regex_lowercase = re.compile(r'[a-z]')
        regex_uppercase = re.compile(r'[A-Z]')
        regex_digit = re.compile(r'[0-9]')
        regex_special = re.compile(r'[\W_]')

        if not regex_lowercase.search(password):
            raise ValueError('Пароль должен содержать строчные латинские буквы')
        if not regex_uppercase.search(password):
            raise ValueError('Пароль должен содержать заглавные латинские буквы')
        if not regex_digit.search(password):
            raise ValueError('Пароль должен содержать цифры')
        if not regex_special.search(password):
            raise ValueError('Пароль должен содержать специальные символы')
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        if len(hashed_password) > 1024:
            raise ValueError('Пароль слишком длинный')
        return hashed_password

    @field_validator("email")
    def email_validate(cls, email):
        try:
            validate_email(email)
        except EmailNotValidError:
            raise ValueError("Неверный адрес электронной почты")
        if len(email) > 100:
            raise ValueError("Слишком длинный адрес электронной почты")
        return email


class User(Id):
    username: str
    email: str
    books_in_library: List[str]


class New_Book(BaseModel):
    title: str
    author: str
    genre: str
    description: str
    year: int = Field(ge=1900, le=2024)


class Book(New_Book):
    id: str


class Session(BaseModel):
    data: dict
    life_time_s: Optional[int] = Field(ge=1)


class SessionNoTime(BaseModel):
    data: dict
