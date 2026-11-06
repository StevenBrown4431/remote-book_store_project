from book_repository import BookRepository
from film_repository import FilmRepository
from flask import session

class TestIndexRoutes:
    def test_get_index_returns_200_ok(self,web_client):
        response = web_client.get("/")
        assert response.status_code == 200

class TestBooksRoutes:
    def test_get_books_returns_200_ok(self, web_client):
        response = web_client.get("/books")
        assert response.status_code == 200

    def test_add_books_returns_200_ok_if_logged_in(self, logged_in_client):
        response = logged_in_client.get("/books/add")
        assert response.status_code == 200

    def test_add_books_redirects_302_if_not_logged_in(self, web_client):
        response = web_client.get("/books/add")
        assert response.status_code == 302
        assert response.location == "/sessions/new"

    def test_get_individual_book_returns_200_ok(self, web_client):
        response = web_client.get("/books/1")
        assert response.status_code == 200

    def test_get_individual_book_return_302_if_not_in_db(self, web_client):
        response = web_client.get("/books/50")
        assert response.status_code == 302
        assert response.location == ("/books")
    
    def test_post_books_redirects_and_doesnt_create_book_if_not_logged_in(self, db_connection, web_client):
        response = web_client.post(
            "/books/add", data={
            "title": "Cat in the Hat", 
            "author": "Dr Seuss", 
            "synopsis": "Two children sitting at home on a rainy day are visited by the Cat in the Hat, who shows them some tricks and games.",
            "rating": 5,
            "image_url": "https://covers.openlibrary.org/b/id/9578-M.jpg",
            "notes": "notes"
            })
        assert response.status_code == 302
        assert response.location == "/sessions/new"
        repo = BookRepository(db_connection)
        books = repo.all()
        assert any(b.author == "Dr Seuss" for b in books) == False

    def test_post_books_defaults_to_none_if_non_digit(self, db_connection, logged_in_client):
        response = logged_in_client.post(
            "/books/add", data={
            "title": "Cat in the Hat", 
            "author": "Dr Seuss", 
            "synopsis": "Two children sitting at home on a rainy day are visited by the Cat in the Hat, who shows them some tricks and games.",
            "rating": "five",
            "image_url": "https://covers.openlibrary.org/b/id/9578-M.jpg",
            "notes": "notes"
            })
        assert response.status_code == 302
        assert response.location == "/books"
        repo = BookRepository(db_connection)
        books = repo.all()
        assert any(b.title == "Cat in the Hat" and 
                b.author == "Dr Seuss" and
                b.synopsis == "Two children sitting at home on a rainy day are visited by the Cat in the Hat, who shows them some tricks and games." and
                b.rating == None and 
                b.image_url == "https://covers.openlibrary.org/b/id/9578-M.jpg" and
                b.notes == "notes" for b in books)

    def test_post_books_redirects_and_creates_book_logged_in(self, db_connection, logged_in_client):
        response = logged_in_client.post(
            "/books/add", data={
            "title": "Cat in the Hat", 
            "author": "Dr Seuss", 
            "synopsis": "Two children sitting at home on a rainy day are visited by the Cat in the Hat, who shows them some tricks and games.",
            "rating": 5,
            "image_url": "https://covers.openlibrary.org/b/id/9578-M.jpg",
            "notes": "notes"
            })
        assert response.status_code == 302
        assert response.location == "/books"
        repo = BookRepository(db_connection)
        books = repo.all()
        assert any(b.title == "Cat in the Hat" and 
                b.author == "Dr Seuss" and
                b.synopsis == "Two children sitting at home on a rainy day are visited by the Cat in the Hat, who shows them some tricks and games." and
                b.rating == 5 and 
                b.image_url == "https://covers.openlibrary.org/b/id/9578-M.jpg" and
                b.notes == "notes" for b in books)

    def test_post_books_missing_title_redirects_back_to_add_books_and_doesnt_add_to_db(self, db_connection, logged_in_client):
        response = logged_in_client.post(
                    "/books/add", data={
                    "title": "", 
                    "author": "Dr Seuss", 
                    "synopsis": "Two children sitting at home on a rainy day are visited by the Cat in the Hat, who shows them some tricks and games.",
                    "rating": 5,
                    "image_url": "https://covers.openlibrary.org/b/id/9578-M.jpg",
                    "notes": "notes"
                    })
        assert response.status_code == 302
        assert response.location == "/books/add"
        repo = BookRepository(db_connection)
        books = repo.all()
        assert any(b.author == "Dr Seuss" for b in books) == False

    def test_post_books_whitespace_author_redirects_back_to_add_books_and_doesnt_add_to_db(self, db_connection, logged_in_client):
        response = logged_in_client.post(
                    "/books/add", data={
                    "title": "The Cat in the Hat", 
                    "author": "     ", 
                    "synopsis": "Two children sitting at home on a rainy day are visited by the Cat in the Hat, who shows them some tricks and games.",
                    "rating": 5,
                    "image_url": "https://covers.openlibrary.org/b/id/9578-M.jpg",
                    "notes": "notes"
                    })
        assert response.status_code == 302
        assert response.location == "/books/add"
        repo = BookRepository(db_connection)
        books = repo.all()
        assert any(b.title == "The Cat in the Hat" for b in books) == False

class TestAuthorsRoutes:
    def test_get_authors_returns_full_author_list(self, web_client):
        response = web_client.get("/authors")
        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json[0]["name"] == "Julia Donaldson"

class TestQuotesRoutes:
    def test_get_quotes_returns_200_ok(self, web_client):
        response = web_client.get("/quotes")
        assert response.status_code == 200

class TestSignupRoutes:
    def test_get_sign_up_returns_200_ok(self, web_client):
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
    def test_get_films_returns_200_ok(self, web_client):
        response = web_client.get("/films")
        assert response.status_code == 200

    def test_post_film_redirects_and_adds_film_to_db(self, db_connection, web_client):
        response = web_client.post("/films", data ={
            "title": "Inception",
            "release_year": "2010"
        })
        assert response.status_code == 302
        assert response.location == "/films"

        repo = FilmRepository(db_connection)
        films = repo.all()
        assert any(f.title == "Inception" and f.release_year == 2010 for f in films)

    def test_post_film_missing_title_redirects_back_and_does_not_insert(self, db_connection, web_client):
        response = web_client.post("/films", data ={
            "title": "",
            "release_year": "2010"
        })
        assert response.status_code == 302
        assert response.location == "/films"

        repo = FilmRepository(db_connection)
        films = repo.all()
        assert any(f.release_year == 2010 for f in films) is False

    def test_post_film_invalid_year_redirects_back_and_does_not_insert(self, db_connection, web_client):
        response = web_client.post("/films", data ={
            "title": "Inception",
            "release_year": "not-a-year"
        })
        assert response.status_code == 302
        assert response.location == "/films"

        repo = FilmRepository(db_connection)
        films = repo.all()
        assert any(f.title == "Inception" for f in films) is False

class TestLoginRoutes:
    def test_get_login_returns_200_ok(self, web_client):
        response = web_client.get("/sessions/new")
        assert response.status_code == 200
    
    def test_log_in_form_with_correct_user_and_password_redirects_to_books(self, web_client):
        response = web_client.post('/sessions', data={
            'username': 'Dorothy',
            'password': 'password1'
            })
        assert response.status_code == 302
        assert response.location == "/books"
        assert session["user_id"] == 1
        assert session["username"] == "Dorothy"

    def test_log_in_form_with_incorrect_password_redirects_to_new_session(self, web_client):
        response = web_client.post('/sessions', data={
            'username': 'Dorothy',
            'password': 'password3'
            })
        assert response.status_code == 302
        assert response.location == "/sessions/new"

    def test_log_in_form_with_incorrect_user_redirects_to_new_session(self, web_client):
        response = web_client.post('/sessions', data={
            'username': 'FakeyMcFake',
            'password': 'password3'
            })
        assert response.status_code == 302
        assert response.location == "/sessions/new"

class TestTeamRoutes:
    def test_get_team_returns_200_ok(self, web_client):
        response = web_client.get("/team")
        assert response.status_code == 200

class TestLogoutRoutes:
    def test_logout_redirects_to_index(self, logged_in_client):
        response = logged_in_client.get("/logout")
        assert response.status_code == 302
        assert response.location == "/"
        assert "user_id" not in session
        assert "username" not in session