from user_repository import UserRepository
from user import User

def test_create_user_is_saved_to_db(db_connection):
    repo = UserRepository(db_connection)
    new_user = User("testuser", "password123")
    repo.save_user(new_user)
    result = db_connection.execute("SELECT * FROM users WHERE username = 'testuser'")
    assert len(result) == 1
    assert result[0]['username'] == 'testuser'
    assert result[0]['password'] == 'password123'

def test_find_by_username_matches_table(db_connection):
    repo = UserRepository(db_connection)
    user = repo.find_user("Dorothy")
    assert user is not None
    assert user.username == "Dorothy"
    assert user.password == "password1"
    assert user.id == 1
    