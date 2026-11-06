from user import User

def test_two_identical_books_are_equal():
    user1 = User("testuser", "password")
    user2 = User("testuser", "password")
    assert user1 == user2

def test_two_none_identical_books_arent_equal():
    user1 = User("testuser", "password")
    user2 = User("testuser2", "password")
    assert user1 is not user2

def test_book_shows_in_intended_format():
    user1 = User("testuser", "password")
    assert repr(user1) == "User(None, testuser, password)"