DROP TABLE IF EXISTS books CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS films CASCADE;

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    synopsis VARCHAR(255),
    rating int,
    image_url TEXT,
    notes VARCHAR(255)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE films (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    release_year int
);

INSERT INTO books (title, author, synopsis, rating, image_url, notes) 
VALUES (
    'The Gruffalo',
    'Julia Donaldson',
    'A clever mouse outwits woodland predators by inventing a terrifying beast called a Gruffalo, only to come face-to-face with the creature he imagined.',
    9,
    'https://covers.openlibrary.org/b/id/10549185-M.jpg',
    'Illustrated by Axel Scheffler'
),
(
    'Ada Twist, Scientist',
    'Andrea Beaty',
    'A boundlessly curious young girl uses the scientific method to solve everyday household mysteries and discover the source of a foul smell.',
    8,
    'https://covers.openlibrary.org/b/id/14304005-M.jpg',
    'Illustrated by David Roberts; part of the Questioneers series'
),
(
    'The Girl Who Drank the Moon',
    'Kelly Barnhill',
    'A young girl accidentally infused with moonlight must learn to master her burgeoning magic when a hunter sets out to kill the benevolent witch who raised her, threatening to expose the town''s dark secrets.',
    9,
    'https://covers.openlibrary.org/b/isbn/9781616205676-M.jpg',
    '2017 Newbery Medal Winner'
),
(
    'Dragons in a Bag',
    'Zetta Elliott',
    'A Brooklyn boy discovers his temporary guardian is an urban witch, pulling him into a secret quest to return three mischievous baby dragons to a magical realm.',
    8,
    'https://covers.openlibrary.org/b/isbn/9781524770457-M.jpg',
    'First book in the Dragons in a Bag series'
);

INSERT INTO films (title, release_year) VALUES ('The Godfather', 1972);
INSERT INTO films (title, release_year) VALUES ('Raiders of the Lost Ark', 1981);
INSERT INTO films (title, release_year) VALUES ('Pulp Fiction', 1994);
INSERT INTO films (title, release_year) VALUES ('Gladiator', 2000);

INSERT INTO users (username, password) VALUES ('Dorothy', 'pbkdf2:sha256:1000000$bBWKCJz5ZDv5yUvC$b329303fdc4581fe36a46c43639ee6bcc21d3a5abc83291021880fef68333323');
INSERT INTO users (username, password) VALUES ('Rose', 'pbkdf2:sha256:1000000$kjuO0RfQYmrUz7el$f8bb848ec1f79dab9675095e28ca5f872c649cded6a07fef2102451d25afc662');
INSERT INTO users (username, password) VALUES ('Blanche', 'pbkdf2:sha256:1000000$qHxiRrRmstRWwK7K$1caa2075ca974c4fd606d10e7ac58fd7177c3d7b4cea697ebaa7a88d2321a524');
INSERT INTO users (username, password) VALUES ('Sofia', 'pbkdf2:sha256:1000000$HxICpq6ihs1xaQFJ$caf343721a57374bf34b5ead592eb130c78e4856a89668432b18ac088c38591b');