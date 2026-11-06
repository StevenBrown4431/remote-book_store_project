from playwright.sync_api import Page, expect

def test_landing_page_displays_heading_and_quotes(page: Page):
    page.goto("http://127.0.0.1:5001/quotes")
    expect(page.locator(".page-title")).to_have_text("Quotes")
    
    quote_items = page.locator(".quote-list li")
    expect(quote_items).to_have_count(5)
    expect(quote_items).to_contain_text([
        'Stephen King: "Books are a uniquely portable magic."',
        'Carl Sagan: "To read is to voyage through time."',
        'George R.R. Martin: "A reader lives a thousand lives before he dies."',
        'Margaret Atwood: "A word after a word after a word is power."',
        'Anna Quindlen: "Books are the plane, and the train, and the road.'
    ])