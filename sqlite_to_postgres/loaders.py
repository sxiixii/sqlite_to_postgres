import sqlite3
from dataclasses import astuple
from sqlite3 import DatabaseError, Row
from typing import Generator

from logger_setup import log
from movies_dataclasses import (
    FilmWorkDataClass,
    GenreDataClass,
    GenreFilmWorkDataClass,
    PersonDataClass,
    PersonFilmWorkDataClass
)
from psycopg2 import Error
from psycopg2.extensions import connection as postgres_connection
from psycopg2.extras import execute_batch
from sql_queries import INSERT_QUERY

TABLES = ('person', 'film_work', 'genre', 'person_film_work', 'genre_film_work')
BATCH_SIZE = 500


class PostgresSaver:
    def __init__(self, connection: postgres_connection):
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.batch_size = BATCH_SIZE

    def save_all_data(self, data: dict):
        try:
            for table in TABLES:
                self._insert_to_table(data[table], table)
        except Error as err:
            log.critical(f'Во время вставки данных в movies_database произошла ошибка: {err}')
            self.conn.rollback()
            raise

    def _insert_to_table(self, data: Generator[tuple, None, None], table: str) -> None:
        self._truncate_table(table)
        log.info(f'Postgres: Очищена таблица "{table}"')
        for item in data:
            item = self._convert_dataclass_to_tuple(item)
            execute_batch(self.cursor, INSERT_QUERY[table], item, page_size=BATCH_SIZE)
            self.conn.commit()
            log.info(f'Postgres: Сохранены записи в таблицу "{table}"')

    def _convert_dataclass_to_tuple(self, data: tuple) -> Generator[tuple, None, None]:
        return (astuple(movie) for movie in data)

    def _truncate_table(self, table):
        self.cursor.execute(f"""TRUNCATE content.{table} CASCADE""")


class SQLiteExtractor:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.conn.row_factory = Row
        self.cursor = self.conn.cursor()

    def extract_movies(self) -> dict[str, list]:
        try:
            movies_data = {
                'person': self._select_from_table_to_dataclass(),
                'film_work': self._extract_film_work_to_dataclass(),
                'genre': self._extract_genre_to_dataclass(),
                'person_film_work': self._extract_person_film_work_to_dataclass(),
                'genre_film_work': self._extract_genre_film_work_to_dataclass(),
            }
            return movies_data
        except DatabaseError as err:
            log.critical(f'Во время извлечения данных из SQLite произошла ошибка: {err}')
            self.conn.rollback()
            raise

    def _select_from_table(self, movie_table: str) -> None:
        self.cursor.execute(f'SELECT * FROM {movie_table};')

    def _select_from_table_to_dataclass(self) -> list[PersonDataClass, ...]:
        self._select_from_table('person')
        list_of_dataclasses = []
        while True:
            persons = self.cursor.fetchmany(BATCH_SIZE)
            if persons:
                for person in persons:
                    person_dataclass = PersonDataClass(
                        id=person['id'],
                        full_name=person['full_name'],
                    )
                    list_of_dataclasses.append(person_dataclass)
                log.info(f'SQLite: Извлечено {len(list_of_dataclasses)} записей из таблицы "person"')
                yield list_of_dataclasses
                list_of_dataclasses = []
            else:
                break

    def _extract_film_work_to_dataclass(self) -> list[FilmWorkDataClass, ...]:
        self._select_from_table('film_work')
        list_of_dataclasses = []
        while True:
            movies = self.cursor.fetchmany(BATCH_SIZE)
            if movies:
                for movie in movies:
                    film_dataclass = FilmWorkDataClass(
                        id=movie['id'],
                        title=movie['title'],
                        description=movie['description'],
                        rating=movie['rating'],
                        type=movie['type'],
                    )
                    list_of_dataclasses.append(film_dataclass)
                log.info(f'SQLite: Извлечено {len(list_of_dataclasses)} записей из таблицы "film_work"')
                yield list_of_dataclasses
                list_of_dataclasses = []
            else:
                break

    def _extract_genre_to_dataclass(self) -> list[GenreDataClass, ...]:
        self._select_from_table('genre')
        list_of_dataclasses = []
        while True:
            genres = self.cursor.fetchmany(BATCH_SIZE)
            if genres:
                for genre in genres:
                    genre_dataclass = GenreDataClass(
                        id=genre['id'],
                        name=genre['name'],
                        description=genre['description']
                    )
                    list_of_dataclasses.append(genre_dataclass)
                log.info(f'SQLite: Извлечено {len(list_of_dataclasses)} записей из таблицы "genre"')
                yield list_of_dataclasses
                list_of_dataclasses = []
            else:
                break

    def _extract_genre_film_work_to_dataclass(self) -> list[GenreFilmWorkDataClass, ...]:
        self._select_from_table('genre_film_work')
        list_of_dataclasses = []
        while True:
            genres_films = self.cursor.fetchmany(BATCH_SIZE)
            if genres_films:
                for genre_film in genres_films:
                    film_genre_dataclass = GenreFilmWorkDataClass(
                        id=genre_film['id'],
                        genre_id=genre_film['genre_id'],
                        film_work_id=genre_film['film_work_id']
                    )
                    list_of_dataclasses.append(film_genre_dataclass)
                log.info(f'SQLite: Извлечено {len(list_of_dataclasses)} записей из таблицы "genre_film_work"')
                yield list_of_dataclasses
                list_of_dataclasses = []
            else:
                break

    def _extract_person_film_work_to_dataclass(self) -> list[PersonFilmWorkDataClass, ...]:
        self._select_from_table('person_film_work')
        list_of_dataclasses = []
        while True:
            persons_films = self.cursor.fetchmany(BATCH_SIZE)
            if persons_films:
                for person_film in persons_films:
                    film_person_dataclass = PersonFilmWorkDataClass(
                        id=person_film['id'],
                        person_id=person_film['person_id'],
                        film_work_id=person_film['film_work_id'],
                        role=person_film['role']
                    )
                    list_of_dataclasses.append(film_person_dataclass)
                log.info(f'SQLite: Извлечено {len(list_of_dataclasses)} записей из таблицы "person_film_work"')
                yield list_of_dataclasses
                list_of_dataclasses = []
            else:
                break
