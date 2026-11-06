from flask import Flask, render_template, request, redirect, session
from database_connection import DatabaseConnection
from book_repository import BookRepository
from book import Book
from user_repository import UserRepository
from user import User
from film_repository import FilmRepository
from film import Film
from login_required import login_required

# instantiate a Flask app object
app = Flask(__name__)
app.secret_key = "some_really_secret_key"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/quotes", methods=["GET"])
def get_quotes():
    return render_template("quotes.html")

@app.route('/books', methods= ['GET'])
def get_all_books():
    connection = DatabaseConnection()
    connection.connect()
    book_repo = BookRepository(connection)
    books = book_repo.all()
    return render_template("books.html", books=books)

@app.route('/books/<int:book_id>', methods=['GET'])
def get_individual_book(book_id):
    connection = DatabaseConnection()
    connection.connect()
    
    book_repo = BookRepository(connection)
    book = book_repo.find_by_id(book_id)

    if not book:
        return redirect("/books")
    return render_template("ind_book.html", book=book) 

@app.route('/books/add', methods=['GET','POST'])
@login_required
def add_book():
    if request.method == 'POST':
        connection = DatabaseConnection()
        connection.connect()
        book_repo = BookRepository(connection)
        
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        synopsis = request.form.get("synopsis", "").strip() or None
        raw_rating = request.form.get("rating","").strip()
        rating = int(raw_rating) if raw_rating.isdigit() else None
        image_url = request.form.get("image_url", "").strip() or None
        notes = request.form.get ("notes", "").strip() or None
        
        book = Book(
            title=title,
            author=author,
            synopsis=synopsis,
            rating=rating,
            image_url=image_url,
            notes=notes
        )
        try:
            book_repo.create(book)
            return redirect("/books")
        except ValueError:
            return redirect("/books/add")

    return render_template("create_book.html")

@app.route('/team', methods=['GET'])
def get_team():
    team = ["Dorothy", "Rose", "Blanche", "Sophia"]
    return render_template("team.html", team=team)

@app.route('/users/new', methods=['GET'])
def get_signup():
    return render_template("sign_up.html")

@app.route('/users/new', methods=['POST'])
def save_user():
    connection = DatabaseConnection()
    connection.connect()
    user_repo = UserRepository(connection)
    user_details = request.form
    user = User(username=user_details["username"], password=user_details["password"])
    user_repo.save_user(user)
    return redirect("/")

@app.route('/sessions/new', methods=['GET'])
def get_login():
    return render_template("log_in.html")

@app.route('/sessions', methods=['POST'])
def login():
    connection = DatabaseConnection()
    connection.connect()
    user_repo = UserRepository(connection)

    username = request.form["username"]
    password = request.form["password"]

    if user_repo.check_password(username, password):
        user = user_repo.find_user(username)
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect("/books")
    else:
        return redirect("/sessions/new")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")

@app.route ('/films', methods=['GET'])
def get_films():
    connection = DatabaseConnection()
    connection.connect()
    film_repo = FilmRepository(connection)
    films = film_repo.all()
    return render_template("films.html", films=films)

@app.route('/films', methods=['POST'])
def add_film():
    connection = DatabaseConnection()
    connection.connect()
    film_repo = FilmRepository(connection)

    title = request.form.get("title", "").strip()
    raw_year = request.form.get("release_year", "").strip()
    release_year = int(raw_year) if raw_year.isdigit() else None

    film = Film(title=title, release_year=release_year)
    
    try:
        film_repo.create(film)
    except ValueError:
        return redirect ("/films")

    return redirect ("/films")

#returns list of authors
@app.route ('/authors', methods = ['GET'])
def get_authors():
    return [
    {
        "name": "Julia Donaldson",
        "dob": "1948-09-16"
    },
    {
        "name": "Andrea Beaty",
        "dob": "1961-10-08"
    },
    {
        "name": "Kelly Barnhill",
        "dob": "1973-01-01"
    },
    {
        "name": "Zetta Elliott",
        "dob": "1979-11-11"
    }
    ]

# make the server run in response to `python app.py`
# on port 5001 (you'll learn more about what this means later)
# and use debug mode so that changing code restarts the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
