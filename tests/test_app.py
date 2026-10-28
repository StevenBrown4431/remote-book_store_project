import sys
import os
from book_repository import BookRepository

# this line is a bit of a hack which allows us to import app without changing anything else
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

# test get books returns 200
def test_get_books_returns_a_200(db_connection):
    db_connection.seed("seeds/books.sql")
    client = app.test_client()
    response = client.get("/books")
    assert response.status_code == 200


# get authors returns 200
def test_get_authors_returns_200(db_connection):
    db_connection.seed("seeds/books.sql")
    client = app.test_client()
    response = client.get('/authors')
    assert response.status_code == 200

# get authors returns all authors
def test_get_authors_returns_all_authors(db_connection):
    db_connection.seed("seeds/books.sql")
    client = app.test_client()
    response = client.get('/authors')

    assert response.json == [
    {
        "name": "Julia Donaldson",
        "dob": "1948-09-16"
    },
    {
        "name": "Andrea Beaty",
        "dob": "1961-10-08"
    },
    {
        "name": "Kelly Barnhill",
        "dob": "1973-01-01"
    },
    {
        "name": "Zetta Elliott",
        "dob": "1979-11-11"
    }
    ]

def test_post_books_creates_record(db_connection):
    db_connection.seed("seeds/books.sql")
    client = app.test_client()
    response = client.post("/books", data={"title": "Cat in the Hat", "author": "Dr Seuss"}) 

    assert response.status_code == 302

    repo = BookRepository(db_connection)
    books = repo.all()
    assert any(
        b.title == "Cat in the Hat" and b.author == "Dr Seuss" 
        for b in books
    )
