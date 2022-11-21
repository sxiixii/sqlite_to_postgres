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

CREATE INDEX IF NOT EXISTS film_work_creation_date ON film_work(creation_date);
CREATE INDEX IF NOT EXISTS film_work_title ON film_work(title);

CREATE TABLE IF NOT EXISTS person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE INDEX IF NOT EXISTS person_full_name ON person(full_name);

CREATE TABLE IF NOT EXISTS genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE INDEX IF NOT EXISTS genre_name ON genre(name);

CREATE TABLE IF NOT EXISTS genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    created timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre_idx ON genre_film_work (film_work_id, genre_id);

CREATE TABLE IF NOT EXISTS person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    role TEXT NOT NULL,
    created timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON person_film_work (film_work_id, person_id);