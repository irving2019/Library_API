import os
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.auth import router as auth_router
from src.routers.books import router as books_router
from src.routers.readers import router as readers_router
from src.routers.borrowed_books import router as borrowed_books_router
from src.database.database import engine
from src.models.models import Base

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management System",
    description="API for managing library books and readers",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth_router, tags=["Authentication"])
app.include_router(books_router, prefix="/books", tags=["Books"])
app.include_router(readers_router, prefix="/readers", tags=["Readers"])
app.include_router(borrowed_books_router, prefix="/borrowed-books", tags=["Borrowed Books"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Library Management System API",
        "docs": "/docs",
        "redoc": "/redoc"
    }