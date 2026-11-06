from book import Book

class BookRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute ('SELECT * FROM books')
        return [Book(r["title"], r["author"], r["synopsis"], r["rating"], r["image_url"], r["notes"], r["id"]) for r in rows]

    def create(self, book):
        if not book.title or not book.title.strip() or not book.author or not book.author.strip():
            raise ValueError("Title and author are required.")
        self._connection.execute(
            'INSERT INTO books (title, author, synopsis, rating, image_url, notes) ' \
            'VALUES (%s, %s, %s, %s, %s, %s)',
            [book.title, book.author, book.synopsis, book.rating, book.image_url, book.notes]
        )
        return None

    def find_by_id(self, book_id):
        rows = self._connection.execute ('SELECT * FROM books WHERE id = %s', [book_id])
        if not rows:
            return None
        r = rows[0]
        return Book(r["title"], r["author"], r["synopsis"], r["rating"], r["image_url"], r["notes"], r["id"])