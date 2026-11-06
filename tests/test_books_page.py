from playwright.sync_api import Page, expect

def test_books_page_displays_heading(page: Page):
    page.goto("http://127.0.0.1:5001/books")
    expect(page.locator(".page-title")).to_have_text("Our Books")

def test_books_page_lists_seeded_titles(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/books")
    book_items = page.locator(".book-list li")
    expect(book_items).to_have_count(4)
    expect(book_items).to_contain_text([
        "The Gruffalo",
        "Ada Twist, Scientist",
        "The Girl Who Drank the Moon",
        "Dragons in a Bag",
    ])

def test_books_page_displays_author_names(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/books")
    book_items = page.locator(".book-list li")
    expect(book_items.filter(has_text="The Gruffalo")).to_contain_text("Julia Donaldson")

def test_books_render_in_card_grid(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/books")
    cards = page.locator(".book-list li.book-card")
    expect(cards).to_have_count(4)

    first_card = cards.first
    expect(first_card).to_contain_text("The Gruffalo")
    expect(first_card).to_contain_text("Julia Donaldson")

    img = first_card.locator("img.book-thumb")
    expect(img).to_have_attribute("src", "https://covers.openlibrary.org/b/id/10549185-M.jpg")
    expect(img).to_have_attribute("alt","The Gruffalo")

def test_add_book_displays_fallback_image_when_no_image(logged_in_page_with_cookie, db_connection):
    logged_in_page_with_cookie.goto("http://127.0.0.1:5001/books/add")

    logged_in_page_with_cookie.get_by_placeholder("Title").fill("Death in the Afternoon")
    logged_in_page_with_cookie.get_by_placeholder("Author").fill("Ernest Hemmingway")
    logged_in_page_with_cookie.get_by_role("button", name="Submit").click()
    
    cards = logged_in_page_with_cookie.locator(".book-list li.book-card")
    expect(cards).to_have_count(5)

    new_card = cards.last
    expect(new_card.locator(".book-info")).to_contain_text("Death in the Afternoon")

    fallback = new_card.locator(".fallback-cover")
    expect(fallback.locator(".fallback-title")).to_have_text("Death in the Afternoon")
    expect(fallback.locator(".fallback-author")).to_have_text("Ernest Hemmingway")