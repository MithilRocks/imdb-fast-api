from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

from database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String(255))
    score = Column(Float)
    director_id = Column(Integer, ForeignKey("directors.id"))

    director = relationship("Director", back_populates="movies")
    genres = relationship(
        'Genre',
        secondary='moviegenrerelation',
        backref='movies',
        cascade='all, delete-orphan'
    )
    
class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String(50), unique=True)

class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String(255), unique=True)

    movies = relationship("Movie", back_populates="director")


class Moviegenrerelation(Base):
    __tablename__ = "moviegenrerelation"
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String(255), unique = True)
    password = Column(String(255))
    is_admin = Column(Boolean, default=False)

# model objects to be used in database queries
movies = Movie.__table__
genres = Genre.__table__
directors = Director.__table__
users = User.__table__
moviegenrerelation = Moviegenrerelation.__table__