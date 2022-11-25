import sqlite3
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor


@contextmanager
def open_sqlite_db(file_name: str):
    conn = sqlite3.connect(file_name)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()


@contextmanager
def open_postgresql_db(dsl: dict):
    conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()
