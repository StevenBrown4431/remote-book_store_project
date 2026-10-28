from book import Book
from book_repository import BookRepository

def test_all_returns_all_seeded_books(db_connection):
    db_connection.seed("seeds/books.sql")
    repository = BookRepository(db_connection)

    books = repository.all()

    assert len(books) == 4
    assert books[0].title == "The Gruffalo"
    assert books[0].author == "Julia Donaldson"
    assert books[-1].title == "Dragons in a Bag"
    assert books[-1].author == "Zetta Elliott"

def test_create_adds_new_book_to_database(db_connection):
    repository = BookRepository(db_connection)
    db_connection.seed("seeds/books.sql")

    new_book = Book("The Da Vinci Code", "Dan Brown")
    repository.create(new_book)
    books = repository.all()
    
    assert any(
        b.title == "The Da Vinci Code" and b.author == "Dan Brown" 
        for b in books
    )