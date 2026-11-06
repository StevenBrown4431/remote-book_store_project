from playwright.sync_api import Page, expect

def test_page_loads_username_password_and_submit(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/sessions/new")
    
    expect(page.get_by_label("Username")).to_be_visible()
    expect(page.get_by_label("Password")).to_be_visible()
    expect(page.get_by_role("button", name="Submit")).to_be_visible()

def test_failed_login_password_redirects_to_login(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/sessions/new")
    page.get_by_placeholder("Username").fill("FakeyMcFake")
    page.get_by_placeholder("Password").fill("password1")
    page.get_by_role("button", name="Submit").click()
    
    expect(page).to_have_url("http://127.0.0.1:5001/sessions/new")

def test_failed_login_password_redirects_to_login(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/sessions/new")
    page.get_by_placeholder("Username").fill("Dorothy")
    page.get_by_placeholder("Password").fill("password4")
    page.get_by_role("button", name="Submit").click()
    
    expect(page).to_have_url("http://127.0.0.1:5001/sessions/new")

def test_page_redirects_to_books_after_successful_login(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/sessions/new")
    
    page.get_by_placeholder("Username").fill("Dorothy")
    page.get_by_placeholder("Password").fill("password1")
    page.get_by_role("button", name="Submit").click()

    expect(page).to_have_url("http://127.0.0.1:5001/books")
    expect(page.locator(".site-nav")).to_contain_text("Welcome, Dorothy")
    expect(page.get_by_role("link", name="Log Out")).to_be_visible
    expect(page.get_by_role("link", name="Log In")).not_to_be_visible
    expect(page.get_by_role("link", name="Sign Up")).not_to_be_visible
