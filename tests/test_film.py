from film import Film

def test_two_identical_books_are_equal():
    film1 = Film("The Da Vinci Code", 2006)
    film2 = Film("The Da Vinci Code", 2006)
    assert film1 == film2

def test_two_none_identical_books_arent_equal():
    film1 = Film("The Da Vinci Code", 2006)
    film2 = Film("Angels & Demons", 2006)
    assert film1 is not film2

def test_book_shows_in_intended_format():
    film1 = Film("The Da Vinci Code", 2006)
    assert repr(film1) == "Film(None, The Da Vinci Code, 2006)"