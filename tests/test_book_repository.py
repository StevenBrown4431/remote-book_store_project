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

    new_book = Book("The Da Vinci Code", "Dan Brown", "this is a synopsis", 7, "http://fake.fake", "some notes")
    repository.create(new_book)
    books = repository.all()
    
    assert Book("The Da Vinci Code", "Dan Brown", "this is a synopsis", 7, "http://fake.fake", "some notes", 5) in books

def test_create_book_with_empty_fields_raises_error(db_connection):
    repository = BookRepository(db_connection)
    new_book = Book("","","","","","","")
    with pytest.raises(ValueError):
        repository.create(new_book)

def test_create_raises_error_when_author_is_whitespace(db_connection):
    repository = BookRepository(db_connection)
    invalid_book = Book("The Da Vinci Code", "   ", "synopsis", 7, "http://fake.fake", "notes")
    
    with pytest.raises(ValueError, match="Title and author are required."):
        repository.create(invalid_book)

def test_create_raises_error_when_title_is_whitespace(db_connection):
    repository = BookRepository(db_connection)
    invalid_book = Book("", "Dan Brown", "synopsis", 7, "http://fake.fake", "notes")
    
    with pytest.raises(ValueError, match="Title and author are required."):
        repository.create(invalid_book)

def test_find_book_with_id_in_db(db_connection):
    repo = BookRepository(db_connection)
    book = repo.find_by_id(1)
    assert book.title == "The Gruffalo"

def test_find_book_with_id_not_in_db_returns_none(db_connection):
    repo = BookRepository(db_connection)
    book = repo.find_by_id(47)
    assert book is None