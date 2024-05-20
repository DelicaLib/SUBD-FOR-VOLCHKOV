from models import models
import random
import string


def randomword(length: int):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def get_random_user_id():
    result = models.db["Users"].aggregate([{'$sample': {'size': 1}}, {'$project': {'_id': 1}}])
    random_book = next(result, None)
    if random_book:
        return random_book['_id']
    else:
        return None


def get_random_book_id():
    result = models.db["Books"].aggregate([{'$sample': {'size': 1}}, {'$project': {'_id': 1}}])
    random_book = next(result, None)
    if random_book:
        return random_book['_id']
    else:
        return None


def generate_random_books_ids():
    length = random.randint(0, 15)
    res = []
    for i in range(length):
        res.append(get_random_book_id())
    return res


def add_random_user():
    username = randomword(random.randint(5, 40))
    email = randomword(random.randint(5, 40)) + "@mail.ru"
    password = randomword(random.randint(5, 40))
    books_in_library = generate_random_books_ids()
    new_user = models.User(username, email, password, books_in_library)
    new_user.save_to_db()


def add_random_book():
    title = randomword(random.randint(5, 100))
    author = " ".join(
        [randomword(random.randint(5, 15)), randomword(random.randint(5, 15)), randomword(random.randint(5, 15))])
    genre = randomword(random.randint(5, 20))
    description = randomword(random.randint(5, 1000))
    year = random.randint(1900, 2024)
    new_book = models.Book(title, author, genre, description, year)
    new_book.save_to_db()


def add_random_exchange_requests():
    sender_id = get_random_user_id()
    receiver_id = get_random_user_id()
    book_id = get_random_book_id()
    status = randomword(random.randint(5, 20))
    new_request = models.ExchangeRequest(sender_id, receiver_id, book_id, status)
    new_request.save_to_db()


def get_user(email: str):
    user = models.db["Users"].find_one({"email": email})
    if user is None:
        return None

    return models.User(user["username"], user["email"],
                       user["password"], user["books_in_library"],
                       str(user["_id"]))


def get_book(title: str):
    book = models.db["Books"].find({"title": title})
    if book is None:
        return None
    res = []
    for i in book:
        cur_book = models.Book(i["title"], i["author"],
                               i["genre"], i["description"],
                               i["year"])
        cur_book.id = i["_id"]
        res.append(cur_book)
    return res


def add_books_to_user(user_id: models.ObjectId, books_id: models.List[models.ObjectId]):
    models.db["Users"].update_one(
        {"_id": user_id},
        {"$push": {"books_in_library": {"$each": books_id}}}
    )


def delete_user(user: models.User):
    models.db["Users"].delete_one({"email": user.email})

