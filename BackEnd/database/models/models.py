from sqlalchemy import ForeignKey, SmallInteger, BigInteger, FLOAT, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, MappedAsDataclass


class Base(DeclarativeBase, MappedAsDataclass):
    pass

#region ENTITIES
class Movie(Base):
    __tablename__ = 'movie'

    movie_id: Mapped[int] = mapped_column("movie_id", primary_key=True, init=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    year: Mapped[int | None] = mapped_column(nullable=True)

    genres: Mapped[list['Genre']] = relationship(secondary='movie_genre', back_populates='movies', default_factory=list)
    #ratings: Mapped[list['Rating']] = relationship(back_populates='movie', cascade='all, delete-orphan', default_factory=list)
    score: Mapped['MovieRating| None'] = relationship(back_populates='movie', uselist=False, viewonly=True)
    tags: Mapped[list['MovieTag']] = relationship(back_populates='movie',  viewonly=True)


class Genre(Base):
    __tablename__ = 'genre'

    genre_id: Mapped[int] = mapped_column("genre_id", primary_key=True, autoincrement=True, init=False)
    genre_name: Mapped[str] = mapped_column("genre_name", Text, nullable=False)

    movies: Mapped[list['Movie']] = relationship(secondary='movie_genre', back_populates='genres', default_factory=list)


class AppUser(Base):
    __tablename__ = 'app_user'

    user_id: Mapped[int] = mapped_column("user_id", primary_key=True, autoincrement=True, init=False)
    username: Mapped[str] = mapped_column(Text, nullable=False)
    pw: Mapped[str] = mapped_column(Text, nullable=False)

    ratings: Mapped[list['Rating']] = relationship(back_populates='user', cascade='all, delete-orphan', default_factory=list)
    tags: Mapped[list['Tag']] = relationship(back_populates='user', cascade='all, delete-orphan', default_factory=list)


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
    recorded_at: Mapped[int | None] = mapped_column(BigInteger, nullable=True, default=None)

    #movie: Mapped['Movie'] = relationship(back_populates='ratings', init=False)
    user: Mapped['AppUser'] = relationship(back_populates='ratings', init=False)

class MovieRating(Base):
    __tablename__ = 'movie_rating'

    movie_id: Mapped[int] = mapped_column("movie_id", ForeignKey('movie.movie_id', ondelete='CASCADE'), primary_key=True)
    rating: Mapped[int] = mapped_column("score", FLOAT, nullable=False)

    movie: Mapped['Movie'] = relationship(back_populates='score')


class Tag(Base):
    __tablename__ = 'tag'

    tag_id: Mapped[int] = mapped_column("tag_id", primary_key=True, autoincrement=True, init=False)
    movie_id: Mapped[int | None] = mapped_column("movie_id", ForeignKey('movie.movie_id', ondelete='CASCADE'), nullable=True, default=None)
    user_id: Mapped[int | None] = mapped_column("user_id", ForeignKey('app_user.user_id', ondelete='CASCADE'), nullable=True, default=None)
    tag: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    recorded_at: Mapped[int | None] = mapped_column(BigInteger, nullable=True, default=None)

    #movie: Mapped['Movie'] = relationship(back_populates='tags', init=False)
    user: Mapped['AppUser'] = relationship(back_populates='tags', init=False)

class MovieTag(Base):
    __tablename__ = 'movie_tag_occurrence'

    movie_id: Mapped[int] = mapped_column("movie_id", ForeignKey('movie.movie_id', ondelete='CASCADE'), primary_key=True)
    clean_tag: Mapped[str] = mapped_column("clean_tag", Text, nullable=False, primary_key=True)

    movie: Mapped['Movie'] = relationship(back_populates='tags')

#endregion