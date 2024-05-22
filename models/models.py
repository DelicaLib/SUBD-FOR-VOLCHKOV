from bson import ObjectId
from typing import List, Optional
from pymongo import MongoClient
from config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client["BookSwapHub"]


class User:
    id: ObjectId

    def __init__(self, username: str,
                 email: str, password: str,
                 books_in_library: List[ObjectId], id: Optional[str] = None):
        self.username = username
        self.email = email
        self.password = password
        self.books_in_library = books_in_library
        self.collection = db['Users']
        self.id = id

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "books_in_library": self.books_in_library
        }

    def save_to_db(self):
        user_data = self.to_dict()
        result = self.collection.insert_one(user_data)
        self.id = result.inserted_id

    def remove_book_from_library(self, book_id):
        if book_id in self.books_in_library:
            self.books_in_library.remove(book_id)
        else:
            print(f"Книга с ID {book_id} не найдена в библиотеке пользователя.")

    def __str__(self):
        return f"User(username='{self.username}', email='{self.email}')"


class Book:
    def __init__(self, title: str, author: str, genre: str, description: str, year: int):
        self.title = title
        self.author = author
        self.genre = genre
        self.description = description
        self.year = year

        self.collection = db['Books']

    def save_to_db(self):
        book_data = self.to_dict()
        result = self.collection.insert_one(book_data)
        self.id = result.inserted_id

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "description": self.description,
            "year": self.year
        }


class ExchangeRequest:
    def __init__(self, sender_id: ObjectId, receiver_id: ObjectId, book_id: ObjectId, status: str):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.book_id = book_id
        self.status = status
        self.collection = db['ExchangeRequests']

    def save_to_db(self):
        request_data = self.to_dict()
        result = self.collection.insert_one(request_data)
        self.id = result.inserted_id

    def to_dict(self):
        return {
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "book_id": self.book_id,
            "status": self.status
        }

