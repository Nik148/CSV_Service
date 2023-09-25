import uvicorn
from fastapi import FastAPI
from passlib.context import CryptContext
from app.routers.auth.routers import router as auth_router
from app.routers.csv.routers import router as csv_router
import app.model

tags_metadata = [
    {
        "name": "Auth",
        "description": "Операции идентификации и аутентификации пользователя",
    },
    {
        "name": "CSV",
        "description": "Работа с csv файлами",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(auth_router)
app.include_router(csv_router)

