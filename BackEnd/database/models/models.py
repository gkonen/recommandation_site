from sqlalchemy import ForeignKey, SmallInteger, BigInteger, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

#region ENTITIES
class Movie(Base):
    __tablename__ = 'movie'

    movieId: Mapped[int] = mapped_column("movieid", primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    year: Mapped[int | None] = mapped_column(nullable=True)

    genres: Mapped[list['Genre']] = relationship(secondary='movie_genre', back_populates='movies')
    ratings: Mapped[list['Rating']] = relationship(back_populates='movie', cascade='all, delete-orphan')
    tags: Mapped[list['Tag']] = relationship(back_populates='movie', cascade='all, delete-orphan')


class Genre(Base):
    __tablename__ = 'genre'

    genreId: Mapped[int] = mapped_column("genreid", primary_key=True, autoincrement=True)
    genreName: Mapped[str] = mapped_column("genrename", Text, nullable=False)

    movies: Mapped[list['Movie']] = relationship(secondary='movie_genre', back_populates='genres')


class AppUser(Base):
    __tablename__ = 'app_user'

    userId: Mapped[int] = mapped_column("userid", primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, nullable=False)
    pw: Mapped[str] = mapped_column(Text, nullable=False)

    ratings: Mapped[list['Rating']] = relationship(back_populates='user', cascade='all, delete-orphan')
    tags: Mapped[list['Tag']] = relationship(back_populates='user', cascade='all, delete-orphan')


# Relationnal table
class MovieGenre(Base):
    __tablename__ = 'movie_genre'

    movieId: Mapped[int] = mapped_column("movieid",ForeignKey('movie.movieid', ondelete='CASCADE'), primary_key=True)
    genreId: Mapped[int] = mapped_column("genreid",ForeignKey('genre.genreid', ondelete='CASCADE'), primary_key=True)
#endregion


#region ACTION TABLE
class Rating(Base):
    __tablename__ = 'rating'

    movieId: Mapped[int] = mapped_column("movieid", ForeignKey('movie.movieid', ondelete='CASCADE'), primary_key=True)
    userId: Mapped[int] = mapped_column("userid", ForeignKey('app_user.userid', ondelete='CASCADE'), primary_key=True)
    rating: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    recorded_at: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    movie: Mapped['Movie'] = relationship(back_populates='ratings')
    user: Mapped['AppUser'] = relationship(back_populates='ratings')


class Tag(Base):
    __tablename__ = 'tag'

    tagId: Mapped[int] = mapped_column("tagid", primary_key=True, autoincrement=True)
    movieId: Mapped[int | None] = mapped_column("movieid", ForeignKey('movie.movieid', ondelete='CASCADE'), nullable=True)
    userId: Mapped[int | None] = mapped_column("userid", ForeignKey('app_user.userid', ondelete='CASCADE'), nullable=True)
    tag: Mapped[str | None] = mapped_column(Text, nullable=True)
    recorded_at: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    movie: Mapped['Movie'] = relationship(back_populates='tags')
    user: Mapped['AppUser'] = relationship(back_populates='tags')
#endregion