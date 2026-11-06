from playwright.sync_api import Page, expect

def test_landing_page_displays_heading_and_team_members(page: Page):
    page.goto("http://127.0.0.1:5001/team")
    expect(page.locator(".page-title")).to_have_text("The Team")
    
    team_items = page.locator(".team-list li")
    expect(team_items).to_have_count(4)
    expect(team_items).to_contain_text([
        'Dorothy',
        'Rose',
        'Blanche',
        'Sophia',
    ])