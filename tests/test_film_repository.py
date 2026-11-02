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