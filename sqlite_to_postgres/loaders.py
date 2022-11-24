from dataclasses import astuple
from sqlite3 import Row

from movies_dataclasses import (
    FilmWorkDataClass,
    GenreDataClass,
    GenreFilmWorkDataClass,
    MovieTable,
    PersonDataClass,
    PersonFilmWorkDataClass
)


class PostgresSaver:
    def __init__(self, connection):
        self.cursor = connection.cursor()

    def save_all_data(self, data):
        self._film_work_saver(data[MovieTable.film_work])
        self._person_saver(data[MovieTable.person])
        self._genre_saver(data[MovieTable.genre])
        self._genre_film_work_saver(data[MovieTable.genre_film_work])
        self._person_film_work_saver(data[MovieTable.person_film_work])

    def _truncate_table(self, movie_table: MovieTable):
        self.cursor.execute(f"""TRUNCATE content.{movie_table}""")

    def _film_work_saver(self, data: list[FilmWorkDataClass, ...]):
        self._truncate_table(MovieTable.film_work)
        args = ','.join(
            self.cursor.mogrify("(%s, %s, %s, %s, %s, NOW(), NOW())", astuple(movie)).decode() for movie in data
        )
        self.cursor.execute(f"""
            INSERT INTO content.film_work (title, description, type, id, rating, created, modified)
            VALUES {args}
            """)

    def _person_saver(self, data: list[PersonDataClass, ...]):
        self._truncate_table(MovieTable.person)
        args = ','.join(
            self.cursor.mogrify("(%s, %s, NOW(), NOW())", astuple(person)).decode() for person in data
        )
        self.cursor.execute(f"""
            INSERT INTO content.person (full_name, id, created, modified)
            VALUES {args}
            """)

    def _genre_saver(self, data: list[GenreDataClass, ...]):
        self._truncate_table(MovieTable.genre)
        args = ','.join(
            self.cursor.mogrify("(%s, %s, %s, NOW(), NOW())", astuple(genre)).decode() for genre in data
        )
        self.cursor.execute(f"""
            INSERT INTO content.genre (name, description, id, created, modified)
            VALUES {args}
            """)

    def _genre_film_work_saver(self, data: list[GenreFilmWorkDataClass, ...]):
        self._truncate_table(MovieTable.genre_film_work)
        args = ','.join(
            self.cursor.mogrify("(%s, %s, %s, NOW())", astuple(genre_film_work)).decode() for genre_film_work in data
        )
        self.cursor.execute(f"""
            INSERT INTO content.genre_film_work (genre_id, film_work_id, id, created)
            VALUES {args}
            """)

    def _person_film_work_saver(self, data: list[PersonFilmWorkDataClass, ...]):
        self._truncate_table(MovieTable.person_film_work)
        args = ','.join(
            self.cursor.mogrify("(%s, %s, %s, %s, NOW())", astuple(person_film)).decode() for person_film in data
        )
        self.cursor.execute(f"""
            INSERT INTO content.person_film_work (person_id, film_work_id, role, id, created)
            VALUES {args}
            """)


class SQLiteExtractor:
    def __init__(self, connection):
        connection.row_factory = Row
        self.cursor = connection.cursor()

    def extract_movies(self) -> dict[str, list]:
        movies_data = {
            MovieTable.film_work: self._extract_film_work_to_dataclass(),
            MovieTable.person: self._extract_person_to_dataclass(),
            MovieTable.genre: self._extract_genre_to_dataclass(),
            MovieTable.person_film_work: self._extract_person_film_work_to_dataclass(),
            MovieTable.genre_film_work: self._extract_genre_film_work_to_dataclass(),
        }
        return movies_data

    def _select_from_table(self, movie_table: MovieTable):
        self.cursor.execute(f'SELECT * FROM {movie_table};')

    def _extract_film_work_to_dataclass(self) -> list[FilmWorkDataClass, ...]:
        self._select_from_table(MovieTable.film_work)
        data = self.cursor.fetchall()
        list_of_dataclasses = []
        for film in data:
            film_dataclass = FilmWorkDataClass(
                id=film['id'],
                title=film['title'],
                description=film['description'],
                rating=film['rating'],
                type=film['type'],
            )
            list_of_dataclasses.append(film_dataclass)
        return list_of_dataclasses

    def _extract_person_to_dataclass(self) -> list[PersonDataClass, ...]:
        self._select_from_table(MovieTable.person)
        persons = self.cursor.fetchall()
        list_of_dataclasses = []
        for person in persons:
            person_dataclass = PersonDataClass(
                id=person['id'],
                full_name=person['full_name'],
            )
            list_of_dataclasses.append(person_dataclass)
        return list_of_dataclasses

    def _extract_genre_to_dataclass(self) -> list[GenreDataClass, ...]:
        self._select_from_table(MovieTable.genre)
        genres = self.cursor.fetchall()
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
        self._select_from_table(MovieTable.genre_film_work)
        films_genres = self.cursor.fetchall()
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
        self._select_from_table(MovieTable.person_film_work)
        persons_film = self.cursor.fetchall()
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
