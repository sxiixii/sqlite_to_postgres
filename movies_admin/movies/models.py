from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = '"content"."genre"'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class FilmType(models.TextChoices):
    MOVIE = 'movie', _('Movie')
    TV_SHOW = 'tv_show', _('TV show')


class FilmWork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'))
    rating = models.FloatField(
        _('rating'),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    type = models.CharField(
        _('type'),
        max_length=10,
        choices=FilmType.choices,
        default=FilmType.MOVIE,
    )
    genres = models.ManyToManyField(
        Genre,
        through='GenreFilmWork',
        verbose_name=_('genre'),
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = '"content"."film_work"'
        verbose_name = _('film')
        verbose_name_plural = _('films')


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = '"content"."genre_film_work"'
        indexes = [
            models.Index(fields=['film_work', 'genre'], name='film_work_genre_idx'),
        ]
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(max_length=255)
    films = models.ManyToManyField(FilmWork, through='PersonFilmWork')

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = '"content"."person"'
        verbose_name = _('person')
        verbose_name_plural = _('persons')


class PersonRole(models.TextChoices):
    ACTOR = 'actor', _('Actor')
    DIRECTOR = 'director', _('Director')
    SCREENWRITER = 'screenwriter', _('Screenwriter')
    PRODUCER = 'producer', _('Producer')
    OPERATOR = 'operator', _('Operator')
    COMPOSER = 'composer', _('Composer')


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey(FilmWork, related_name='person_film', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(
        _('role'),
        max_length=50,
        choices=PersonRole.choices,
        default=PersonRole.ACTOR,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"content"."person_film_work"'
        indexes = [
            models.Index(fields=['person', 'film_work', 'role'], name='person_film_work_role_idx'),
        ]
