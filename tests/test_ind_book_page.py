from playwright.sync_api import Page, expect

def test_ind_book_page_displays_book_name(page: Page):
    page.goto("http://127.0.0.1:5001/books/1")
    expect(page.locator(".detail-title")).to_have_text("The Gruffalo")

def test_ind_book_page_displays_back_link_redirects_to_all_books(page: Page):
    page.goto("http://127.0.0.1:5001/books/1")
    expect(page.locator(".back-link")).to_contain_text("Back to all books")
    page.locator(".back-link").click()
    expect(page).to_have_url("http://127.0.0.1:5001/books")

def test_ind_book_page_displays_all_info(page: Page):
    page.goto("http://127.0.0.1:5001/books/1")
    expect(page.locator(".detail-title")).to_be_visible()
    expect(page.locator(".detail-author")).to_be_visible()
    expect(page.locator(".detail-rating")).to_be_visible()
    expect(page.locator(".detail-synopsis")).to_be_visible()
    expect(page.locator(".detail-notes")).to_be_visible()
    expect(page.locator(".book-detail-cover")).to_be_visible()
