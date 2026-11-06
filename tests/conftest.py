import pytest
from database_connection import DatabaseConnection
from playwright.sync_api import Page, BrowserContext
from app import app

# This is a Pytest fixture.
# A fixture is a reusable function that provides setup 
# logic for tests, supplying data or state before a test 
# runs and cleaning up afterward.
#
# In our project, it creates an object that we can use in our tests.
# We will use it to create a database connection.

@pytest.fixture
def db_connection():
    conn = DatabaseConnection()
    conn.connect()
    conn.seed("seeds/books.sql")
    return conn

@pytest.fixture
def web_client():
    """Provides a clean Flask test client without instantiating it in every test."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def logged_in_client(web_client):
    """Provides a web_client that already has user session keys populated."""
    with web_client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["username"] = "Dorothy"
    return web_client

@pytest.fixture
def logged_in_page_with_cookie(context: BrowserContext, page:Page):
    serializer = app.session_interface.get_signing_serializer(app)
    session_cookie_val = serializer.dumps({"user_id": 1, "username": "Dorothy"})

    context.add_cookies([{
        "name": "session",
        "value": session_cookie_val,
        "domain": "127.0.0.1",
        "path": "/"
    }])

    return page
