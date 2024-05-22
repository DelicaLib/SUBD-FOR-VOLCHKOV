
from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/error")
async def get_error():
    try:
        raise ValueError("TestError1337 полная жесть")
    except ValueError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="INTERNAL SERVER ERROR")

