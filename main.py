from fastapi import FastAPI

from api_lab3 import LoggingMiddleware
from routes.lab1 import router as lab1_router
from routes.lab2 import router as lab2_router
from routes.lab3 import router as lab3_router


app = FastAPI(title="SUBD Labs",
              docs_url="/docs",
              redoc_url="/redoc",
              swagger_ui_init_oauth=None,
              swagger_ui_parameters=None,
              swagger_ui_oauth2_redirect_url=None,
              swagger_ui_version="5.9.0"
              )
app.add_middleware(LoggingMiddleware)


app.include_router(lab1_router, prefix="/lab1")
app.include_router(lab2_router, prefix="/lab2")
app.include_router(lab3_router, prefix="/lab3")
