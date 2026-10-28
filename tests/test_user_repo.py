import sys
import os
from database_connection import DatabaseConnection
from app import app

def test_create_user_is_saved_to_db(db_connection):
    db_connection.seed("seeds/books.sql")
    client = app.test_client()
    response = client.post('/users/new', data={
        'username': 'testuser',
        'password': 'password123'
        })
    assert response.status_code == 302

    result = db_connection.execute("SELECT * FROM users WHERE username = 'testuser'")
    assert len(result) == 1
    assert result[0]['username'] == 'testuser'
    assert result[0]['password'] == 'password123'