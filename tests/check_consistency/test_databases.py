import sqlite3
from os import environ

import psycopg2
import pytest
from dotenv import load_dotenv

load_dotenv()

dsl = {
    'dbname': environ.get('DB_NAME'),
    'user': environ.get('DB_USER'),
    'password': environ.get('DB_PASSWORD'),
    'host': environ.get('DB_HOST', '127.0.0.1'),
    'port': environ.get('DB_PORT', 5432),
    'options': '-c search_path=content',
}


@pytest.fixture
def setup_databases():
    pg_connect = psycopg2.connect(**dsl)
    pg_cursor = pg_connect.cursor()
    pg_cursor.execute('''SET search_path TO content, public;''')

    sqlt_connect = sqlite3.connect(environ.get('SQLT_DB_NAME'))
    sqlt_cursor = sqlt_connect.cursor()

    yield pg_cursor, sqlt_cursor
    pg_connect.close()
    sqlt_connect.close()


def test_number_of_records_in_film_work_tables(setup_databases):
    pg_cur, sqlt_cur = setup_databases
    query = '''SELECT COUNT(*) FROM film_work'''
    pg_cur.execute(query)
    sqlt_cur.execute(query)
    pg_number_of_records = pg_cur.fetchone()
    sqlt_number_of_records = sqlt_cur.fetchone()
    assert pg_number_of_records[0] == sqlt_number_of_records[0]


def test_number_of_records_in_person_tables(setup_databases):
    pg_cur, sqlt_cur = setup_databases
    query = '''SELECT COUNT(*) FROM person'''
    pg_cur.execute(query)
    sqlt_cur.execute(query)
    pg_number_of_records = pg_cur.fetchone()
    sqlt_number_of_records = sqlt_cur.fetchone()
    assert pg_number_of_records[0] == sqlt_number_of_records[0]


def test_number_of_records_in_genre_tables(setup_databases):
    pg_cur, sqlt_cur = setup_databases
    query = '''SELECT COUNT(*) FROM genre'''
    pg_cur.execute(query)
    sqlt_cur.execute(query)
    pg_number_of_records = pg_cur.fetchone()
    sqlt_number_of_records = sqlt_cur.fetchone()
    assert pg_number_of_records[0] == sqlt_number_of_records[0]


def test_number_of_records_in_person_film_work_tables(setup_databases):
    pg_cur, sqlt_cur = setup_databases
    query = '''SELECT COUNT(*) FROM person_film_work'''
    pg_cur.execute(query)
    sqlt_cur.execute(query)
    pg_number_of_records = pg_cur.fetchone()
    sqlt_number_of_records = sqlt_cur.fetchone()
    assert pg_number_of_records[0] == sqlt_number_of_records[0]


def test_number_of_records_in_genre_film_work_tables(setup_databases):
    pg_cur, sqlt_cur = setup_databases
    query = '''SELECT COUNT(*) FROM genre_film_work'''
    pg_cur.execute(query)
    sqlt_cur.execute(query)
    pg_number_of_records = pg_cur.fetchone()
    sqlt_number_of_records = sqlt_cur.fetchone()
    assert pg_number_of_records[0] == sqlt_number_of_records[0]


def test_match_records_in_genre_tables(setup_databases):
    pg_cur, sqlt_cur = setup_databases
    query = '''SELECT id, name, description FROM genre'''
    pg_cur.execute(query)
    sqlt_cur.execute(query)
    pg_number_of_records = pg_cur.fetchall()
    sqlt_number_of_records = sqlt_cur.fetchall()
    assert set(sqlt_number_of_records) == set(pg_number_of_records)


def test_match_records_in_person_tables(setup_databases):
    pg_cur, sqlt_cur = setup_databases
    query = '''SELECT id, full_name FROM person'''
    pg_cur.execute(query)
    sqlt_cur.execute(query)
    pg_number_of_records = pg_cur.fetchall()
    sqlt_number_of_records = sqlt_cur.fetchall()
    assert set(sqlt_number_of_records) == set(pg_number_of_records)


def test_match_records_in_film_work_tables(setup_databases):
    pg_cur, sqlt_cur = setup_databases
    query = '''SELECT id, title, description, creation_date, rating, type FROM film_work'''
    pg_cur.execute(query)
    sqlt_cur.execute(query)
    pg_number_of_records = pg_cur.fetchall()
    sqlt_number_of_records = sqlt_cur.fetchall()
    assert set(sqlt_number_of_records) == set(pg_number_of_records)


def test_match_records_in_person_film_work_tables(setup_databases):
    pg_cur, sqlt_cur = setup_databases
    query = '''SELECT id, person_id, film_work_id, role FROM person_film_work'''
    pg_cur.execute(query)
    sqlt_cur.execute(query)
    pg_number_of_records = pg_cur.fetchall()
    sqlt_number_of_records = sqlt_cur.fetchall()
    assert set(sqlt_number_of_records) == set(pg_number_of_records)


def test_match_records_in_genre_film_work_tables(setup_databases):
    pg_cur, sqlt_cur = setup_databases
    query = '''SELECT id, genre_id, film_work_id FROM genre_film_work'''
    pg_cur.execute(query)
    sqlt_cur.execute(query)
    pg_number_of_records = pg_cur.fetchall()
    sqlt_number_of_records = sqlt_cur.fetchall()
    assert set(sqlt_number_of_records) == set(pg_number_of_records)
