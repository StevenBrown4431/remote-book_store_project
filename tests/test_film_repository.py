from film import Film
from film_repository import FilmRepository
import pytest

def test_all_returns_all_seeded_films(db_connection):
    repository = FilmRepository(db_connection)
    films = repository.all()

    assert len(films) == 4
    assert films[0].title == "The Godfather"
    assert films[0].release_year == 1972
    assert films[-1].title == "Gladiator"
    assert films[-1].release_year == 2000

def test_create_adds_new_film_to_db(db_connection):
    repo = FilmRepository(db_connection)

    new_film = Film("The Da Vinci Code", 2006)
    repo.create(new_film)
    films = repo.all()

    assert any(f.title == "The Da Vinci Code" and f.release_year == 2006 for f in films)

def test_create_film_with_empty_title_raises_error(db_connection):
    repo = FilmRepository(db_connection)
    with pytest.raises(ValueError, match= "Title and release year are required."):
        repo.create(Film("", 2006))

def test_create_film_with_empty_release_year_raises_error(db_connection):
    repo = FilmRepository(db_connection)
    with pytest.raises(ValueError, match= "Title and release year are required."):
        repo.create(Film("The Da Vinci Code", None))

def test_create_film_with_whitespace_title_raises_error(db_connection):
    repo = FilmRepository(db_connection)
    with pytest.raises(ValueError, match= "Title and release year are required."):
        repo.create(Film("    ", 2006))