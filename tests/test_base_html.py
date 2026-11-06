from playwright.sync_api import Page, expect

def test_unauthenticated_nav_state_renders_public_links(page: Page):
    page.goto("http://127.0.0.1:5001/")
    nav = page.locator(".site-nav")

    expected_links = ["Home", "Books", "Films", "Authors", "Quotes", "Team", "Sign Up", "Log In"]
    for link_text in expected_links:
        expect(nav.get_by_role("link", name=link_text)).to_be_visible()

    # Verify authenticated items are absent
    expect(page.locator(".nav-user")).not_to_be_visible()
    expect(nav.get_by_role("link", name="Log Out")).not_to_be_visible()


def test_authenticated_nav_state_renders_greeting_and_logout(logged_in_page_with_cookie):
    logged_in_page_with_cookie.goto("http://127.0.0.1:5001/")
    nav = logged_in_page_with_cookie.locator(".site-nav")

    expect(logged_in_page_with_cookie.locator(".nav-user")).to_have_text("Welcome, Dorothy")
    expect(nav.get_by_role("link", name="Log Out")).to_be_visible()

    expect(nav.get_by_role("link", name="Sign Up")).not_to_be_visible()
    expect(nav.get_by_role("link", name="Log In")).not_to_be_visible()


def test_nav_links_route_to_correct_paths(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/")

    page.locator(".site-nav").get_by_role("link", name="Films").click()
    expect(page).to_have_url("http://127.0.0.1:5001/films")

    page.locator(".site-nav").get_by_role("link", name="Books").click()
    expect(page).to_have_url("http://127.0.0.1:5001/books")

    page.locator(".site-nav").get_by_role("link", name="Quotes").click()
    expect(page).to_have_url("http://127.0.0.1:5001/quotes")

    page.locator(".site-nav").get_by_role("link", name="Team").click()
    expect(page).to_have_url("http://127.0.0.1:5001/team")