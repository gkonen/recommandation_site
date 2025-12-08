from sqlalchemy import ForeignKey, SmallInteger, BigInteger, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

#region ENTITIES
class Movie(Base):
    __tablename__ = 'movie'

    movie_id: Mapped[int] = mapped_column("movie_id", primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    year: Mapped[int | None] = mapped_column(nullable=True)

    genres: Mapped[list['Genre']] = relationship(secondary='movie_genre', back_populates='movies')
    ratings: Mapped[list['Rating']] = relationship(back_populates='movie', cascade='all, delete-orphan')
    tags: Mapped[list['Tag']] = relationship(back_populates='movie', cascade='all, delete-orphan')


class Genre(Base):
    __tablename__ = 'genre'

    genre_id: Mapped[int] = mapped_column("genre_id", primary_key=True, autoincrement=True)
    genre_name: Mapped[str] = mapped_column("genre_name", Text, nullable=False)

    movies: Mapped[list['Movie']] = relationship(secondary='movie_genre', back_populates='genres')


class AppUser(Base):
    __tablename__ = 'app_user'

    user_id: Mapped[int] = mapped_column("user_id", primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, nullable=False)
    pw: Mapped[str] = mapped_column(Text, nullable=False)

    ratings: Mapped[list['Rating']] = relationship(back_populates='user', cascade='all, delete-orphan')
    tags: Mapped[list['Tag']] = relationship(back_populates='user', cascade='all, delete-orphan')


# Relational table
class MovieGenre(Base):
    __tablename__ = 'movie_genre'

    movie_id: Mapped[int] = mapped_column("movie_id",ForeignKey('movie.movie_id', ondelete='CASCADE'), primary_key=True)
    genre_id: Mapped[int] = mapped_column("genre_id",ForeignKey('genre.genre_id', ondelete='CASCADE'), primary_key=True)
#endregion


#region ACTION TABLE
class Rating(Base):
    __tablename__ = 'rating'

    movie_id: Mapped[int] = mapped_column("movie_id", ForeignKey('movie.movie_id', ondelete='CASCADE'), primary_key=True)
    user_id: Mapped[int] = mapped_column("user_id", ForeignKey('app_user.user_id', ondelete='CASCADE'), primary_key=True)
    rating: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    recorded_at: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    movie: Mapped['Movie'] = relationship(back_populates='ratings')
    user: Mapped['AppUser'] = relationship(back_populates='ratings')


class Tag(Base):
    __tablename__ = 'tag'

    tag_id: Mapped[int] = mapped_column("tag_id", primary_key=True, autoincrement=True)
    movie_id: Mapped[int | None] = mapped_column("movie_id", ForeignKey('movie.movie_id', ondelete='CASCADE'), nullable=True)
    user_id: Mapped[int | None] = mapped_column("user_id", ForeignKey('app_user.user_id', ondelete='CASCADE'), nullable=True)
    tag: Mapped[str | None] = mapped_column(Text, nullable=True)
    recorded_at: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    movie: Mapped['Movie'] = relationship(back_populates='tags')
    user: Mapped['AppUser'] = relationship(back_populates='tags')
#endregion