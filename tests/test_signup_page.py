from playwright.sync_api import Page, expect

def test_book_form_submission_redirects_to_index(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/users/new")
    page.get_by_placeholder("Username").fill('testuser')
    page.get_by_placeholder("Password").fill('password123')
    page.get_by_role("button", name="Submit").click()
    
    expect(page).to_have_url("http://127.0.0.1:5001/")