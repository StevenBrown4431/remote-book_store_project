from book import Book
from book_repository import BookRepository
import pytest

def test_all_returns_all_books(db_connection):
    repository = BookRepository(db_connection)
    books = repository.all()

    assert len(books) == 4
    assert books[0].title == "The Gruffalo"
    assert books[0].author == "Julia Donaldson"
    assert books[-1].title == "Dragons in a Bag"
    assert books[-1].author == "Zetta Elliott"

def test_create_adds_new_book_to_database(db_connection):
    repository = BookRepository(db_connection)

    new_book = Book("The Da Vinci Code", "Dan Brown")
    repository.create(new_book)
    books = repository.all()
    
    assert any(b.title == "The Da Vinci Code" and b.author == "Dan Brown" for b in books)

def test_create_book_with_empty_fields_raises_error(db_connection):
    repository = BookRepository(db_connection)
    new_book = Book("","")
    with pytest.raises(ValueError):
        repository.create(new_book)