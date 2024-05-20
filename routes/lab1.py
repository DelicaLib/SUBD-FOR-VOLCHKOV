import models.models
import api_lab1

from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from models import schemas


router = APIRouter()


@router.post("/generate/users/{count}")
async def generate_users(count: int):
    for i in range(count):
        api_lab1.add_random_user()
    return JSONResponse(status_code=status.HTTP_200_OK, content="Пользователи созданы")


@router.post("/generate/books/{count}")
async def generate_books(count: int):
    for i in range(count):
        api.add_random_book()
    return JSONResponse(status_code=status.HTTP_200_OK, content="Книги созданы")


@router.post("/generate/exchange_requests/{count}")
async def generate_exchange_requests(count: int):
    for i in range(count):
        api_lab1.add_random_exchange_requests()
    return JSONResponse(status_code=status.HTTP_200_OK, content="Запросы обмена созданы")


@router.get("/user/{email}", response_model=schemas.User)
async def get_user(email: str):
    found_user = api_lab1.get_user(email)
    if found_user is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="Пользователь не найден")
    return schemas.User(id=str(found_user.id),
                        username=found_user.username,
                        email=found_user.email,
                        books_in_library=[str(i) for i in found_user.books_in_library])


@router.post("/user")
async def new_user(user_data: schemas.New_user):
    found_user = api_lab1.get_user(user_data.email)
    if found_user is not None:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content="Пользователь с такой почтой уже зарегистрирован")

    new_user = api_lab1.models.User(user_data.username, user_data.email,
                               user_data.password, [])
    new_user.save_to_db()
    return JSONResponse(status_code=status.HTTP_200_OK, content="Пользователь создан")


@router.post("/book")
async def new_book(book_data: schemas.New_Book):
    new_book = api_lab1.models.Book(book_data.title, book_data.author,
                               book_data.genre, book_data.description,
                               book_data.year)
    new_book.save_to_db()
    return JSONResponse(status_code=status.HTTP_200_OK, content="Книга создана")


@router.get("/book/{title}", response_model=schemas.List[schemas.Book])
async def get_book(title: str):
    found_books = api_lab1.get_book(title)
    if found_books is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="Книги не найдены")
    res = []
    for i in found_books:
        res.append(schemas.Book(id=str(i.id), title=i.title,
                                author=i.author, genre=i.genre,
                                description=i.description, year=i.year))
    return res


@router.patch("/user/add_book")
async def add_books_to_user(books_id: schemas.List[str], email: str):
    user = api_lab1.get_user(email)
    if user is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="Пользователь не найден")
    api_lab1.add_books_to_user(models.models.ObjectId(user.id), [models.models.ObjectId(i) for i in books_id])
    return JSONResponse(status_code=status.HTTP_200_OK, content="Книги добавлены")


@router.delete("/user")
async def delete_user(email: str):
    user = api_lab1.get_user(email)
    if user is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="Пользователь не найден")
    api_lab1.delete_user(user)
    return JSONResponse(status_code=status.HTTP_200_OK, content="Пользователь удалён")
