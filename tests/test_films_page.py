from playwright.sync_api import Page, expect

def test_films_page_displays_heading(page: Page):
    page.goto("http://127.0.0.1:5001/films")
    expect(page.locator(".page-title")).to_have_text("Our Films")

def test_films_page_lists_seeded_titles(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/films")
    film_items = page.locator(".film-list li")
    expect(film_items).to_have_count(4)
    expect(film_items).to_contain_text([
        "The Godfather",
        "Raiders of the Lost Ark",
        "Pulp Fiction",
        "Gladiator",
    ])

def test_films_page_displays_release_years(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/films")
    film_items = page.locator(".film-list li")
    expect(film_items).to_contain_text([
            "1972",
            "1981",
            "1994",
            "2000",
        ])
def test_films_render_in_card_grid(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/films")
    cards = page.locator(".film-card")
    expect(cards).to_have_count(4)

    first_card = cards.first
    expect(first_card).to_contain_text("The Godfather")
    expect(first_card).to_contain_text("1972")

    img = first_card.locator("img.film-thumb")
    expect(img).to_have_attribute("src", "/static/images/film_1.jpg")
    expect(img).to_have_attribute("alt","The Godfather")

def test_film_displays_fallback_image_when_no_image(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/films")
    
    cards = page.locator(".film-card")
    expect(cards).to_have_count(4)

    last_card = cards.last
    expect(last_card.locator(".film-info")).to_contain_text("Gladiator")

    fallback = last_card.locator(".fallback-cover")
    expect(fallback.locator(".fallback-title")).to_have_text("Gladiator")
    expect(fallback.locator(".fallback-release_year")).to_have_text("2000")

def test_submitting_film_form_appends_card_to_page(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/films")

    film_cards = page.locator(".film-card")
    expect(film_cards).to_have_count(4)

    page.get_by_placeholder("Title").fill("Jurassic Park")
    page.get_by_placeholder("Release Year").fill("1993")
    page.get_by_role("button", name="Add Film").click()

    expect(page).to_have_url("http://127.0.0.1:5001/films")

    expect(film_cards).to_have_count(5)
    new_card = film_cards.last
    expect(new_card.locator(".film-info")).to_contain_text("Jurassic Park")
    expect(new_card.locator(".film-info")).to_contain_text("1993")

def test_empty_film_submission_does_not_add_card(page: Page, db_connection):
    page.goto("http://127.0.0.1:5001/films")

    page.get_by_role("button", name="Add Film").click()

    page.goto("http://127.0.0.1:5001/films")
    expect(page.locator(".film-card")).to_have_count(4)