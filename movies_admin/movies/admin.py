from django.contrib import admin

from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'id')


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    autocomplete_fields = ('genre',)


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    autocomplete_fields = ('person',)


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)
    list_display = (
        'title',
        'type',
        'creation_date',
        'rating',
        'get_genres',
        'get_actors',
        'get_directors',
    )
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')
    list_prefetch_related = ('genres', 'person_set', 'person_film')

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])

    def get_actors(self, obj):
        person_idx = [film.person_id for film in obj.person_film.all() if film.role == 'actor']
        actors = [person.full_name for person in obj.person_set.all() if person.id in person_idx]
        return ', '.join(actor for actor in actors)

    def get_directors(self, obj):
        person_idx = [film.person_id for film in obj.person_film.all() if film.role == 'director']
        director = [person.full_name for person in obj.person_set.all() if person.id in person_idx]
        return ', '.join(actor for actor in director)

    get_genres.short_description = 'Жанры'
    get_actors.short_description = 'Актеры'
    get_directors.short_description = 'Режиссеры'


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name', 'id')
