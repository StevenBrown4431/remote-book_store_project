from user import User

class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def save_user(self, user):
        self._connection.execute(
            'INSERT INTO users (username, password) VALUES (%s, %s)',
            [user.username, user.password]
        )
        return None

    def find_user(self, username):
        user_details = self._connection.execute(
            'SELECT * FROM users WHERE username = %s',
            [username]
        )[0]
        return User(
            user_details["username"],
            user_details["password"],
            user_details["id"]
        )
