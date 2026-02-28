from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/books", tags=["books"])


class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int


books_db = [
    Book(id=1, title="Война и мир", author="Лев Толстой", year=1869),
    Book(id=2, title="1984", author="Джордж Оруэлл", year=1949),
]


@router.get("/", response_model=List[Book])
async def read_books():
    return books_db


@router.get("/{book_id}", response_model=Book)
async def read_book(book_id: int):
    """Показать книгу"""
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")


@router.post("/", response_model=Book, status_code=201)
async def create_book(book: Book):
    """Создание книги"""
    if any(b.id == book.id for b in books_db):
        raise HTTPException(status_code=400, detail="Книга с таким ID уже существует")
    books_db.append(book)
    return book
