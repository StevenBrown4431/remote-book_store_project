from book_repository import BookRepository
from user_repository import UserRepository


class TestBooksRoutes:
    def test_get_books_returns_200_ok(self, db_connection, web_client):
        response = web_client.get("/books")
        assert response.status_code == 200

    def test_post_books_redirects_and_doesnt_create_book_not_logged_in(self, db_connection, web_client):
        response = web_client.post("/books", data={"title": "Cat in the Hat", "author": "Dr Seuss"})
        assert response.status_code == 302
        assert response.location == "/sessions/new"
        repo = BookRepository(db_connection)
        books = repo.all()
        assert any(b.title == "Cat in the Hat" and b.author == "Dr Seuss" for b in books) == False
    
    def test_post_books_redirects_and_creates_book_logged_in(self, db_connection, logged_in_client):
        response = logged_in_client.post("/books", data={"title": "Cat in the Hat", "author": "Dr Seuss"})
        assert response.status_code == 302
        assert response.location == "/books"
        repo = BookRepository(db_connection)
        books = repo.all()
        assert any(b.title == "Cat in the Hat" and b.author == "Dr Seuss" for b in books)

class TestAuthorsRoutes:
    def test_get_authors_returns_full_author_list(self, db_connection, web_client):
        response = web_client.get("/authors")
        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json[0]["name"] == "Julia Donaldson"

class TestQuotesRoutes:
    def test_get_quotes_returns_200_ok(self, db_connection, web_client):
        response = web_client.get("/quotes")
        assert response.status_code == 200

class TestSignupRoutes:
    def test_get_sign_up_returns_200_ok(self, db_connection, web_client):
        response = web_client.get("/users/new")
        assert response.status_code == 200

    def test_create_user_adds_to_user_db_and_redirects_to_index(self, db_connection, web_client):
        response = web_client.post('/users/new', data={
            'username': 'testuser',
            'password': 'password123'
            })
        assert response.status_code == 302
        assert response.location == "/"

        result = db_connection.execute("SELECT * FROM users WHERE username = 'testuser'")
        assert len(result) == 1
        assert result[0]["username"] == "testuser"

class TestFilmRoutes:
    def test_get_quotes_returns_200_ok(self, db_connection, web_client):
        response = web_client.get("/films")
        assert response.status_code == 200

class TestLoginRoutes:
    def test_get_login_returns_200_ok(self, db_connection, web_client):
        response = web_client.get("/sessions/new")
        assert response.status_code == 200
    
    def test_log_in_form_with_correct_user_and_password_redirects_to_books(self, db_connection, web_client):
        response = web_client.post('/sessions', data={
            'username': 'Dorothy',
            'password': 'password1'
            })
        assert response.status_code == 302
        assert response.location == "/books"

    def test_log_in_form_with_incorrect_user_and_password_redirects_to_new_session(self, db_connection, web_client):
        response = web_client.post('/sessions', data={
            'username': 'Dorothy',
            'password': 'password3'
            })
        assert response.status_code == 302
        assert response.location == "/sessions/new"