from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class FilmWorkDataClass:
    title: str
    description: str
    type: str
    id: UUID = field(default_factory=uuid4)
    rating: float = field(default=0.0)


@dataclass(frozen=True)
class PersonDataClass:
    full_name: str
    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class GenreDataClass:
    name: str
    description: str
    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class GenreFilmWorkDataClass:
    genre_id: UUID
    film_work_id: UUID
    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class PersonFilmWorkDataClass:
    person_id: UUID
    film_work_id: UUID
    role: str
    id: UUID = field(default_factory=uuid4)
