import sqlite3
from os import environ

from dotenv import load_dotenv
from psycopg2.extensions import connection as postgres_connection

from loaders import PostgresSaver, SQLiteExtractor
from context_managers import open_postgresql_db, open_sqlite_db


def load_from_sqlite(sqlite_connection: sqlite3.Connection, pg_connection: postgres_connection):
    sqlite_extractor = SQLiteExtractor(sqlite_connection)
    data = sqlite_extractor.extract_movies()
    postgres_saver = PostgresSaver(pg_connection)
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
    SQLITE_DB = environ.get('SQLT_DB_NAME')

    with open_sqlite_db(SQLITE_DB) as sqlite_conn, open_postgresql_db(dsl) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
