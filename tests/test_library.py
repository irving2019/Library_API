import pytest
from fastapi import status
from src.auth.auth import create_access_token

def test_create_user(client):
    response = client.post(
        "/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "email" in response.json()

def test_create_book(client):
    # Сначала создаем пользователя и получаем токен
    client.post(
        "/register",
        json={"email": "librarian@example.com", "password": "password123"}
    )
    response = client.post(
        "/token",
        data={"username": "librarian@example.com", "password": "password123"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Теперь создаем книгу
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "publication_year": 2020,
        "isbn": "1234567890",
        "copies_available": 2
    }
    response = client.post("/books/", json=book_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == book_data["title"]

def test_borrow_book_limit(client, test_db):
    # Создаем пользователя и получаем токен
    client.post(
        "/register",
        json={"email": "librarian@example.com", "password": "password123"}
    )
    response = client.post(
        "/token",
        data={"username": "librarian@example.com", "password": "password123"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Создаем читателя
    reader_data = {
        "name": "Test Reader",
        "email": "reader@example.com"
    }
    reader_response = client.post("/readers/", json=reader_data, headers=headers)
    reader_id = reader_response.json()["id"]

    # Создаем 4 книги
    books = []
    for i in range(4):
        book_data = {
            "title": f"Book {i}",
            "author": "Author",
            "copies_available": 1
        }
        book_response = client.post("/books/", json=book_data, headers=headers)
        books.append(book_response.json()["id"])

    # Пытаемся взять 4 книги
    for i, book_id in enumerate(books):
        borrow_data = {
            "book_id": book_id,
            "reader_id": reader_id
        }
        response = client.post("/borrow/", json=borrow_data, headers=headers)
        
        if i < 3:
            assert response.status_code == 200
        else:
            # Четвертая книга должна быть отклонена
            assert response.status_code == 400
            assert "maximum number of borrowed books" in response.json()["detail"]

def test_return_nonexistent_book(client):
    # Создаем пользователя и получаем токен
    client.post(
        "/register",
        json={"email": "librarian@example.com", "password": "password123"}
    )
    response = client.post(
        "/token",
        data={"username": "librarian@example.com", "password": "password123"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Пытаемся вернуть несуществующую книгу
    response = client.post("/return/999", headers=headers)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
