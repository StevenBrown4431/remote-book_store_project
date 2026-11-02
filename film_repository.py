from film import Film

class FilmRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute ('SELECT * FROM films')
        return [Film(r["title"], r["release_year"], r["id"]) for r in rows]
