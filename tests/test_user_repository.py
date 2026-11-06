from werkzeug.security import check_password_hash, generate_password_hash
from user_repository import UserRepository
from user import User

def test_user_initializes_with_hashed_password(db_connection):
    user = User("testuser", "scrypt:32768:8:1$samplehash", id=1)
    assert user.username == "testuser"
    assert user.password == "scrypt:32768:8:1$samplehash"
    assert user.id == 1

def test_save_user_hashes_password_in_db(db_connection):
    repo = UserRepository(db_connection)

    plain_pass = "supersecret123"
    user = User("alice", plain_pass)
    repo.save_user(user)

    rows = db_connection.execute("SELECT password FROM users WHERE username = %s", ["alice"])
    stored_hash = rows[0]["password"]

    assert stored_hash != plain_pass
    assert check_password_hash(stored_hash, plain_pass) is True

def test_check_password_returns_true_for_valid_password(db_connection):
    repo = UserRepository(db_connection)

    user = repo.find_user("Dorothy")
    assert repo.check_password("Dorothy", "password1") is True

def test_check_password_returns_false_for_invalid_password(db_connection):
    repo = UserRepository(db_connection)

    assert repo.check_password("Dorothy", "wrong_password") is False
    assert repo.check_password("NonExistentUser", "password1") is False

# def test_create_user_is_saved_to_db(db_connection):
#     repo = UserRepository(db_connection)
#     new_user = User("testuser", "password123")
#     repo.save_user(new_user)
#     result = db_connection.execute("SELECT * FROM users WHERE username = 'testuser'")
#     assert len(result) == 1
#     assert result[0]['username'] == 'testuser'
#     assert result[0]['password'] == 'password123'

# def test_find_by_username_matches_table(db_connection):
#     repo = UserRepository(db_connection)
#     user = repo.find_user("Dorothy")
#     assert user is not None
#     assert user.username == "Dorothy"
#     assert user.password == "scrypt:32768:8:1$samplehash"
#     assert user.id == 1

# def test_find_by_username_returns_none_if_doesnt_exist(db_connection):
#     repo = UserRepository(db_connection)
#     user = repo.find_user("fakeymcfake")
#     assert user == None