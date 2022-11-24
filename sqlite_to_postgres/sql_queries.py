INSERT_QUERY = {
    'film_work': '''INSERT INTO content.film_work (title, description, type, id, rating, created, modified)
                    VALUES (%s, %s, %s, %s, %s, NOW(), NOW())''',
    'person': '''INSERT INTO content.person (full_name, id, created, modified) VALUES (%s, %s, NOW(), NOW())''',
    'genre': '''INSERT INTO content.genre (name, description, id, created, modified)
                VALUES (%s, %s, %s, NOW(), NOW())''',
    'genre_film_work': '''INSERT INTO content.genre_film_work (genre_id, film_work_id, id, created)
                          VALUES (%s, %s, %s, NOW())''',
    'person_film_work': '''INSERT INTO content.person_film_work (person_id, film_work_id, role, id, created)
                           VALUES (%s, %s, %s, %s, NOW())'''
}
