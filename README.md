# Лабораторные работы по СУБД

Чтобы запустить код необходимо установить пакеты из requirements.txt

Также необходимо установить и запустить redis сервер, mongoDB сервер и создать бд в MongoDB.

Создать .env файл и написать следующие переменные, но со своими данными:

```bash 
MONGO_URL="mongodb://localhost:27017/"
REDIS_HOST="localhost"
REDIS_PORT="6379"
REDIS_DB="0"
CLICKHOUSE_HOST="localhost"
```

### Структура БД в mongoDB

Название БД: BookSwapHub

Документ User:

    _id: ObjectID
    username: string
    email: string
    password: string
    books_in_library: Array

Документ Books:

    _id: ObjectID
    title: string
    author: string
    genre: string
    description: Array
    year: integer

Документ ExchangeRequests:

    _id: ObjectID
    sender_id: ObjectID
    receiver_id: ObjectID
    book_id: ObjectID
    status: string

### Запуск fastAPI

```bash
uvicorn main:app
```

Посмотреть документацию можно в host:port/docs, где host и port - это хост и порт вашего сервера fastAPI