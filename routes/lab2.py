import asyncio

import redis
import json

from fastapi import APIRouter
from models import schemas
from fastapi import status
from fastapi.responses import JSONResponse


router = APIRouter()
r = redis.Redis(host='localhost', port=6379, db=0)

with open('redis-script.lua', 'r') as file:
    script = file.read()

script_sha = r.script_load(script)


@router.post("/session")
async def create_session(session_data: schemas.Session):
    data = list(map(str, [item for pair in session_data.data.items() for item in pair]))
    keys_count = 2 + len(data)
    print(data)
    life_time = "" if session_data.life_time_s is None else str(session_data.life_time_s)

    result = r.evalsha(script_sha, keys_count,
                       "CREATE", life_time,
                       *data)
    print(result)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(result.decode("utf-8")))


@router.patch("/session")
async def update_session(session_id: str, session_data: schemas.Session):
    data = list(map(str, [item for pair in session_data.data.items() for item in pair]))
    keys_count = 3 + len(data)
    print(data)
    life_time = "" if session_data.life_time_s is None else str(session_data.life_time_s)

    result = r.evalsha(script_sha, keys_count,
                       "UPDATE", session_id,
                       life_time, *data)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(result.decode("utf-8")))


@router.delete("/session")
async def stop_session(session_id: str):
    result = r.evalsha(script_sha, 2, "END", session_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content="Сессия удалена")


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    result = r.evalsha(script_sha, 2,
                       "CHECK", session_id)
    result_dict = json.loads(result)
    return JSONResponse(status_code=status.HTTP_200_OK, content=result_dict)


@router.delete("/clear")
async def clear_redis():
    result = r.flushall()
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK, content="Redis очищен")
    else:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Redis не очистился")


@router.get("/all_data")
async def get_all_redis_data():
    cursor, keys = r.scan(0)
    result = json.dumps([key.decode('utf-8') for key in keys])
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
