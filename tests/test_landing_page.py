from playwright.sync_api import Page, expect

def test_landing_page_displays_heading(page: Page):
    page.goto("http://127.0.0.1:5001")
    expect(page.locator(".page-title")).to_have_text("AceReads")