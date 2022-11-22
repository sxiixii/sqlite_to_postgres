from os import path

from django.conf import settings


def film_work_path():
    return path.join(settings.BASE_DIR, 'media', 'film_works')