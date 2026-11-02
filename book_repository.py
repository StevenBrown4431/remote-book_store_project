from book import Book

class BookRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute ('SELECT * FROM books')
        return [Book(r["title"], r["author"], r["id"]) for r in rows]

    def create(self, book):
        if not book.title or not book.title.strip() or not book.author or not book.author.strip():
            raise ValueError("Title and author are required.")
        self._connection.execute(
            'INSERT INTO books (title, author) VALUES (%s, %s)',
            [book.title, book.author]
        )
        return None
