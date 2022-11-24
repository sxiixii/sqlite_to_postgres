import sqlite3
from os import environ

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as pg_connection
from psycopg2.extras import DictCursor

from loaders import PostgresSaver, SQLiteExtractor


def load_from_sqlite(sqlite_conn: sqlite3.Connection, pg_conn: pg_connection):
    sqlite_extractor = SQLiteExtractor(sqlite_conn)
    data = sqlite_extractor.extract_movies()
    postgres_saver = PostgresSaver(pg_conn)
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    load_dotenv()
    dsl = {
        'dbname': environ.get('DB_NAME'),
        'user': environ.get('DB_USER'),
        'password': environ.get('DB_PASSWORD'),
        'host': environ.get('DB_HOST', '127.0.0.1'),
        'port': environ.get('DB_PORT', 5432),
        'options': '-c search_path=content',
    }
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
