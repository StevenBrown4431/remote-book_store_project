from playwright.sync_api import Page, expect

def test_add_book_redirects_to_login_if_not_logged_in(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/books/add")
    expect(page).to_have_url("http://127.0.0.1:5001/sessions/new")

def test_book_form_empty_doesnt_add_book(logged_in_page_with_cookie, db_connection):
    logged_in_page_with_cookie.goto("http://127.0.0.1:5001/books/add")
    logged_in_page_with_cookie.get_by_role("button", name="Submit").click()

    logged_in_page_with_cookie.goto("http://127.0.0.1:5001/books")
    book_items = logged_in_page_with_cookie.locator(".book-list li")
    expect(book_items).to_have_count(4)

def test_book_form_submission_appends_book_list(logged_in_page_with_cookie, db_connection):
    logged_in_page_with_cookie.goto("http://127.0.0.1:5001/books/add")
    logged_in_page_with_cookie.get_by_placeholder("Title").fill("Death in the Afternoon")
    logged_in_page_with_cookie.get_by_placeholder("Author").fill("Ernest Hemmingway")
    logged_in_page_with_cookie.get_by_role("button", name="Submit").click()
    book_items = logged_in_page_with_cookie.locator(".book-list li")
    expect(book_items).to_have_count(5)
    expect(book_items.filter(has_text="Death in the Afternoon")).to_contain_text("Ernest Hemmingway")

def test_book_form_submission_adds_new_cover_art_either_link_or_fallback(logged_in_page_with_cookie, db_connection):
    logged_in_page_with_cookie.goto("http://127.0.0.1:5001/books/add")
    logged_in_page_with_cookie.get_by_placeholder("Title").fill("Death in the Afternoon")
    logged_in_page_with_cookie.get_by_placeholder("Author").fill("Ernest Hemmingway")
    logged_in_page_with_cookie.get_by_placeholder("Synopsis").fill("Explores the history, rules, and ritual of Spanish bullfighting (corridas de toros).")
    logged_in_page_with_cookie.get_by_placeholder("Rating").fill("4")
    logged_in_page_with_cookie.get_by_placeholder("https://example.com/cover.jpg").fill("https://covers.openlibrary.org/b/id/5951738-M.jpg")
    logged_in_page_with_cookie.get_by_placeholder("Notes").fill("")
    logged_in_page_with_cookie.get_by_role("button", name="Submit").click()
    cards = logged_in_page_with_cookie.locator(".book-list li.book-card")
    expect(cards).to_have_count(5)

    last_card = cards.last
    expect(last_card).to_contain_text("Death in the Afternoon")
    expect(last_card).to_contain_text("Ernest Hemmingway")

    img = last_card.locator("img.book-thumb")
    expect(img).to_have_attribute("src", "https://covers.openlibrary.org/b/id/5951738-M.jpg")
    expect(img).to_have_attribute("alt","Death in the Afternoon")

    fallback = last_card.locator(".fallback-cover")
    expect(fallback.locator(".fallback-title")).to_have_text("Death in the Afternoon")
    expect(fallback.locator(".fallback-author")).to_have_text("Ernest Hemmingway")