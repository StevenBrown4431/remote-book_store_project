from user import User
from werkzeug.security import generate_password_hash, check_password_hash

class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def save_user(self, user):
        hashed_password = generate_password_hash(user.password, method="pbkdf2:sha256")
        self._connection.execute(
            'INSERT INTO users (username, password) VALUES (%s, %s)',
            [user.username, hashed_password]
        )
        return None

    def find_user(self, username):
        rows = self._connection.execute(
            'SELECT * FROM users WHERE username = %s', [username])
        if not rows:
            return None
        row = rows[0]
        return User(row["username"], row["password"], row["id"])

    def check_password(self, username, password):
        user = self.find_user(username)
        if not user:
            return False
        return check_password_hash(user.password, password)