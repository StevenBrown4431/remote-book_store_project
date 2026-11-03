from playwright.sync_api import Page, expect

def test_books_page_displays_heading(page: Page):
    page.goto("http://127.0.0.1:5001/films")
    expect(page.locator(".page-title")).to_have_text("Our Films")

def test_books_page_lists_seeded_titles(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/films")
    film_items = page.locator(".film-list li")
    expect(film_items).to_have_count(4)
    expect(film_items).to_contain_text([
        "The Godfather",
        "Raiders of the Lost Ark",
        "Pulp Fiction",
        "Gladiator",
    ])