from playwright.sync_api import Page, expect
from book import Book
from book_repository import BookRepository

def test_has_title(page: Page):
    page.goto("http://127.0.0.1:5001/books")

    h1 = page.locator("h1")

    expect(h1).to_have_text("Our Books")

def test_has_list_of_books(page: Page, db_connection):
    db_connection.seed("seeds/books.sql")
    page.goto("http://127.0.0.1:5001/books")
    book_items = page.locator(".book-list li")
    expect(book_items).to_have_count(4)

    expect(book_items).to_contain_text([
        "The Gruffalo",
        "Ada Twist, Scientist",
        "The Girl Who Drank the Moon",
        "Dragons in a Bag",
    ])

def test_has_added_created_book(page: Page, db_connection):
    db_connection.seed("seeds/books.sql")
    repository = BookRepository(db_connection)
    new_book = Book("The Hobbit", "J.R.R. Tolkien")
    repository.create(new_book)
    page.goto("http://127.0.0.1:5001/books")
    book_items = page.locator(".book-list li")
    expect(book_items).to_have_count(5)
    expect(book_items).to_contain_text(["The Hobbit"])

def test_books_page_displays_author_names(page: Page, db_connection):
    db_connection.seed("seeds/books.sql")
    page.goto("http://127.0.0.1:5001/books")

    book_items = page.locator(".book-list li")

    expect(book_items.filter(has_text="The Gruffalo")).to_contain_text(
        "Julia Donaldson"
    )
    expect(
        book_items.filter(has_text="Ada Twist, Scientist")
    ).to_contain_text("Andrea Beaty")

def test_form_interaction_and_table_update(page: Page, db_connection):
    db_connection.seed("seeds/books.sql")
    page.goto("http://127.0.0.1:5001/books")
    page.get_by_placeholder("Title").fill("View from the Afternoon")
    page.get_by_placeholder("Author").fill("Ernest Hemmingway")
    page.get_by_role("button", name="Submit").click()
    book_items = page.locator(".book-list li")
    expect(book_items).to_have_count(5)
    expect(book_items.filter(has_text="View from the Afternoon")).to_contain_text(
            "Ernest Hemmingway"
        )