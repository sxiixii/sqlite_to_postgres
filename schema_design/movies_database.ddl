CREATE SCHEMA IF NOT EXISTS content;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

SET search_path TO content, public;

CREATE TABLE IF NOT EXISTS film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT not null,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL REFERENCES genre (id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES film_work (id) ON DELETE CASCADE,
    created timestamp with time zone
);

CREATE TABLE IF NOT EXISTS person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid NOT NULL REFERENCES person (id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES film_work (id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    created timestamp with time zone
);

CREATE INDEX IF NOT EXISTS film_work_title ON film_work(title);
CREATE INDEX IF NOT EXISTS film_work_rating_creation_date ON film_work(rating, creation_date);
CREATE INDEX IF NOT EXISTS person_full_name ON person(full_name);
CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre_idx ON genre_film_work (film_work_id, genre_id);
CREATE UNIQUE INDEX IF NOT EXISTS person_film_work_role_idx ON person_film_work (person_id, film_work_id, role);
