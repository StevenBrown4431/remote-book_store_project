DROP TABLE IF EXISTS books CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS films CASCADE;

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255)
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

INSERT INTO books (title, author) VALUES ('The Gruffalo', 'Julia Donaldson');
INSERT INTO books (title, author) VALUES ('Ada Twist, Scientist', 'Andrea Beaty');
INSERT INTO books (title, author) VALUES ('The Girl Who Drank the Moon', 'Kelly Barnhill');
INSERT INTO books (title, author) VALUES ('Dragons in a Bag', 'Zetta Elliott');

INSERT INTO users (username, password) VALUES ('Dorothy', 'password1');
INSERT INTO users (username, password) VALUES ('Rose', 'password2');
INSERT INTO users (username, password) VALUES ('Blanche', 'password3');
INSERT INTO users (username, password) VALUES ('Sofia', 'password4');

INSERT INTO films (title, release_year) VALUES ('The Godfather', 1972);
INSERT INTO films (title, release_year) VALUES ('Raiders of the Lost Ark', 1981);
INSERT INTO films (title, release_year) VALUES ('Pulp Fiction', 1994);
INSERT INTO films (title, release_year) VALUES ('Gladiator', 2000);