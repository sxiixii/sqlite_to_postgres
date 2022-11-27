import sqlite3
from dataclasses import astuple, dataclass
from sqlite3 import DatabaseError, Row
from typing import Generator

from logger_setup import log
from movies_dataclasses import MOVIE_DATACLASS
from psycopg2 import Error
from psycopg2.extensions import connection as postgres_connection
from psycopg2.extras import execute_batch
from sql_queries import INSERT_QUERY

BATCH_SIZE = 500


class PostgresSaver:
    def __init__(self, connection: postgres_connection):
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.batch_size = BATCH_SIZE

    def save_all_data(self, data: dict[str, dataclass]):
        try:
            for table in MOVIE_DATACLASS.keys():
                self._insert_to_table(data[table], table)
        except Error as err:
            log.critical(f'Во время вставки данных в movies_database произошла ошибка: {err}')
            self.conn.rollback()
            raise

    def _insert_to_table(self, data: Generator[tuple, None, None], table: str) -> None:
        log.info(f'Postgres: Очищена таблица "{table}"')
        for item in data:
            item = self._convert_dataclass_to_tuple(item)
            execute_batch(self.cursor, INSERT_QUERY[table], item, page_size=BATCH_SIZE)
            self.conn.commit()
            log.info(f'Postgres: Сохранены записи в таблицу "{table}"')

    def _convert_dataclass_to_tuple(self, data: tuple) -> Generator[tuple, None, None]:
        return (astuple(movie) for movie in data)


class SQLiteExtractor:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.conn.row_factory = Row
        self.cursor = self.conn.cursor()

    def extract_movies(self):
        try:
            movies_data = {}
            for table, movie_dataclass in MOVIE_DATACLASS.items():
                movies_data[table] = self.__select_from_table_to_dataclass(table, movie_dataclass)
            return movies_data
        except DatabaseError as err:
            log.critical(f'Во время извлечения данных из SQLite произошла ошибка: {err}')
            self.conn.rollback()
            raise

    def __select_from_table_to_dataclass(self, table: str, movie_dataclass: dataclass):
        self.cursor.execute(f'SELECT * FROM {table};')
        list_of_dataclasses = []
        while True:
            persons = self.cursor.fetchmany(BATCH_SIZE)
            if persons:
                for person in persons:
                    dataclass_fields = movie_dataclass.__annotations__.keys()
                    dataclass_values = [person[field] for field in dataclass_fields]
                    dataclass_instance = movie_dataclass(*dataclass_values)
                    list_of_dataclasses.append(dataclass_instance)
                log.info(f'SQLite: Извлечено {len(list_of_dataclasses)} записей из таблицы "{table}"')
                yield list_of_dataclasses
                list_of_dataclasses = []
            else:
                break
