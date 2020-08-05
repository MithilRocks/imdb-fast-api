from sqlalchemy.orm import Session
from database import database
import models, schemas

async def get_movie(id: int):
    movie = await database.fetch_one(query=models.movies.select().where(models.movies.c.id == id))
    director = await database.fetch_one(query=models.directors.select().where(models.directors.c.id == movie.director_id))
    # genres = await database.fetch_all(query=models.moviegenrerelation.select().where(models.moviegenrerelation.c.movie_id == movie.id))
    genres = await database.fetch_all(
        query=models.moviegenrerelation.select()
        .where(models.moviegenrerelation.c.movie_id == movie.id)
    )
    genre_ids = [x.genre_id for x in genres]
    genre_all = await database.fetch_all(
        query=models.genres.select()
        .where(models.genres.c.id.in_(genre_ids))
    )
    return {"id":movie.id,"name":movie.name,"score":movie.score,"director":director, "genres":genre_all}

async def get_movie_by_name(name: str):
    movie = await database.fetch_one(query=models.movies.select().where(models.movies.c.name == name))
    if not movie:
        return {}
    director = await database.fetch_one(query=models.directors.select().where(models.directors.c.id == movie.director_id))
    # genres = await database.fetch_all(query=models.moviegenrerelation.select().where(models.moviegenrerelation.c.movie_id == movie.id))
    genres = await database.fetch_all(
        query=models.moviegenrerelation.select()
        .where(models.moviegenrerelation.c.movie_id == movie.id)
    )
    genre_ids = [x.genre_id for x in genres]
    genre_all = await database.fetch_all(
        query=models.genres.select()
        .where(models.genres.c.id.in_(genre_ids))
    )
    return {"id":movie.id,"name":movie.name,"score":movie.score,"director":director, "genres":genre_all}

async def get_movies(skip: int = 0, limit: int = 100):
    return await database.fetch_all(query=models.movies.select().offset(skip).limit(limit))

async def create_movie(movie: schemas.MovieCreate):
    movie_c = models.movies.insert().values({"name":movie.name, "score":movie.score, "director_id":movie.director})
    pk = await database.execute(movie_c)
    for genre_id in movie.genres:
        await database.execute(models.moviegenrerelation.insert().values({"movie_id":pk, "genre_id":genre_id}))
    return {**movie.dict()}