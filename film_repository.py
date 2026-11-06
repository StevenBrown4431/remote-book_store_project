from film import Film

class FilmRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute ('SELECT * FROM films')
        return [Film(r["title"], r["release_year"], r["id"]) for r in rows]

    def create(self, film):
        if not film.title or not film.title.strip() or not film.release_year:
            raise ValueError("Title and release year are required.")
        
        self._connection.execute(
            'INSERT INTO films (title, release_year) VALUES (%s, %s)',
            [film.title, film.release_year]
        )
        return None
