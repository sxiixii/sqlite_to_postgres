from dataclasses import astuple
from sqlite3 import DatabaseError, Row

from psycopg2 import Error
from psycopg2.extras import execute_batch

from movies_dataclasses import (FilmWorkDataClass, GenreDataClass,
                                GenreFilmWorkDataClass, PersonDataClass,
                                PersonFilmWorkDataClass)
from sql_queries import INSERT_QUERY

TABLES = ('film_work', 'person', 'genre', 'person_film_work', 'genre_film_work')


class PostgresSaver:
    def __init__(self, connection, page_size=5000):
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.page_size = page_size

    def save_all_data(self, data: dict):
        try:
            for table in TABLES:
                self._insert_to_table(self._convert_dataclass_to_tuple(data[table]), table)
        except Error as err:
            print(f'Во время вставки данных в movies_database произошла ошибка\n{err}')
            self.conn.rollback()

    def _insert_to_table(self, data, table: str):
        self._truncate_table(table)
        self._batch_inserting(self.cursor, INSERT_QUERY[table], data)

    def _convert_dataclass_to_tuple(self, data):
        return (astuple(movie) for movie in data)

    def _truncate_table(self, movie_table: str):
        self.cursor.execute(f"""TRUNCATE content.{movie_table} CASCADE""")

    def _batch_inserting(self, cursor, query: str, data):
        execute_batch(cursor, query, data, page_size=self.page_size)
        self.conn.commit()


class SQLiteExtractor:
    def __init__(self, connection):
        self.conn = connection
        self.conn.row_factory = Row
        self.cursor = self.conn.cursor()

    def extract_movies(self) -> dict[str, list]:
        try:
            movies_data = {
                'film_work': self._extract_film_work_to_dataclass(),
                'person': self._extract_person_to_dataclass(),
                'genre': self._extract_genre_to_dataclass(),
                'person_film_work': self._extract_person_film_work_to_dataclass(),
                'genre_film_work': self._extract_genre_film_work_to_dataclass(),
            }
            return movies_data
        except DatabaseError as err:
            print(f'Во время извлечения данных из sqlite произошла ошибка\n{err}')
            self.conn.rollback()

    def _select_from_table(self, movie_table: str) -> list[dict, ...]:
        self.cursor.execute(f'SELECT * FROM {movie_table};')
        return self.cursor.fetchall()

    def _extract_film_work_to_dataclass(self) -> list[FilmWorkDataClass, ...]:
        movies = self._select_from_table('film_work')
        list_of_dataclasses = []
        for movie in movies:
            film_dataclass = FilmWorkDataClass(
                id=movie['id'],
                title=movie['title'],
                description=movie['description'],
                rating=movie['rating'],
                type=movie['type'],
            )
            list_of_dataclasses.append(film_dataclass)
        return list_of_dataclasses

    def _extract_person_to_dataclass(self) -> list[PersonDataClass, ...]:
        persons = self._select_from_table('person')
        list_of_dataclasses = []
        for person in persons:
            person_dataclass = PersonDataClass(
                id=person['id'],
                full_name=person['full_name'],
            )
            list_of_dataclasses.append(person_dataclass)
        return list_of_dataclasses

    def _extract_genre_to_dataclass(self) -> list[GenreDataClass, ...]:
        genres = self._select_from_table('genre')
        list_of_dataclasses = []
        for genre in genres:
            genre_dataclass = GenreDataClass(
                id=genre['id'],
                name=genre['name'],
                description=genre['description']
            )
            list_of_dataclasses.append(genre_dataclass)
        return list_of_dataclasses

    def _extract_genre_film_work_to_dataclass(self) -> list[GenreFilmWorkDataClass, ...]:
        films_genres = self._select_from_table('genre_film_work')
        list_of_dataclasses = []
        for film_genre in films_genres:
            film_genre_dataclass = GenreFilmWorkDataClass(
                id=film_genre['id'],
                genre_id=film_genre['genre_id'],
                film_work_id=film_genre['film_work_id']
            )
            list_of_dataclasses.append(film_genre_dataclass)
        return list_of_dataclasses

    def _extract_person_film_work_to_dataclass(self) -> list[PersonFilmWorkDataClass, ...]:
        persons_film = self._select_from_table('person_film_work')
        list_of_dataclasses = []
        for person_film in persons_film:
            film_person_dataclass = PersonFilmWorkDataClass(
                id=person_film['id'],
                person_id=person_film['person_id'],
                film_work_id=person_film['film_work_id'],
                role=person_film['role']
            )
            list_of_dataclasses.append(film_person_dataclass)
        return list_of_dataclasses
