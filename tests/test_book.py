from book import Book

def test_two_identical_books_are_equal():
    book1 = Book("The Da Vinci Code", "Dan Brown", "this is a synopsis", 7, "http://fake.fake", "some notes")
    book2 = Book("The Da Vinci Code", "Dan Brown", "this is a synopsis", 7, "http://fake.fake", "some notes")
    assert book1 == book2

def test_two_none_identical_books_arent_equal():
    book1 = Book("The Da Vinci Code", "Dan Brown", "this is a synopsis", 7, "http://fake.fake", "some notes")
    book2 = Book("Angels & Demons", "Dan Brown", "this is a synopsis", 7, "http://fake.fake", "some notes")
    assert book1 is not book2

def test_book_shows_in_intended_format():
    book1 = Book("The Da Vinci Code", "Dan Brown", "this is a synopsis", 7, "http://fake.fake", "some notes")
    assert repr(book1) == "Book(None, The Da Vinci Code, Dan Brown, this is a synopsis, 7, http://fake.fake, some notes)"