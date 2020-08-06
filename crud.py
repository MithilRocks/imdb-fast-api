from sqlalchemy.orm import Session
from database import database
import models, schemas
import copy
from typing import List

async def get_user(username: str):
    return await database.fetch_one(query=models.users.select().where(models.users.c.username == username))
    
async def get_director(id: int):
    return await database.fetch_one(query=models.directors.select().where(models.directors.c.id == id))

async def get_directors(skip: int = 0, limit: int = 100):
    return await database.fetch_all(query=models.directors.select().offset(skip).limit(limit))

async def get_genres(skip: int = 0, limit: int = 100):
    return await database.fetch_all(query=models.genres.select().offset(skip).limit(limit))

async def get_movie_genres(movie_id: int):
    genres = await database.fetch_all(
        query=models.moviegenrerelation.select()
        .where(models.moviegenrerelation.c.movie_id == movie_id)
    )
    genre_ids = [x.genre_id for x in genres]
    return await database.fetch_all(
        query=models.genres.select()
        .where(models.genres.c.id.in_(genre_ids))
    )

async def get_movie(id: int):
    movie = await database.fetch_one(query=models.movies.select().where(models.movies.c.id == id))
    if not movie:
        return {}
    director = await get_director(movie.director_id)
    genres = await get_movie_genres(movie.id)
    return {"id":movie.id,"name":movie.name,"score":movie.score,"popularity":movie.score*10,"director":director, "genres":genres}

async def get_movie_by_name(name: str):
    movie = await database.fetch_one(query=models.movies.select().where(models.movies.c.name == name))
    if not movie:
        return {}
    director = await get_director(movie.director_id)
    genres = await get_movie_genres(movie.id)
    return {"id":movie.id,"name":movie.name,"score":movie.score,"popularity":movie.score*10,"director":director, "genres":genres}

async def get_movies(skip: int = 0, limit: int = 100):
    return await database.fetch_all(query=models.movies.select().offset(skip).limit(limit))

async def create_movie(movie: schemas.MovieCreate):
    movie_c = models.movies.insert().values({"name":movie.name, "score":movie.score, "director_id":movie.director_id})
    pk = await database.execute(movie_c)
    for genre_id in movie.genres_id:
        await database.execute(models.moviegenrerelation.insert().values({"movie_id":pk, "genre_id":genre_id}))
    return {**movie.dict()}

async def delete_movie(movie_id: int):
    return await database.execute(query=models.movies.delete().where(models.movies.c.id == movie_id))

async def update_movie(movie: schemas.MovieUpdateFinal):
    movie_temp = copy.deepcopy(movie)
    if movie.genres_id or movie.genres_id == []:
        await database.execute(query=models.moviegenrerelation.delete().where(models.moviegenrerelation.c.movie_id == movie.id))
        for genre_id in movie.genres_id:
            await database.execute(models.moviegenrerelation.insert().values({"movie_id":movie.id, "genre_id":genre_id}))
        del(movie.genres_id)
    await database.execute(models.movies.update().values(**movie.dict(exclude_unset=True)).where(models.movies.c.id == movie.id))
    return {**movie_temp.dict(exclude_unset=True)}

async def bulk_update_movies(movies: List[schemas.BulkMovies]):
    for movie in movies:
        genres = []
        for genre in movie.genre:
            result = await database.fetch_one(query=models.genres.select().where(models.genres.c.name == genre))
            if result:
                genres.append(result.id)
            else:
                genre_c = models.genres.insert().values({"name":genre})
                pk = await database.execute(genre_c) 
                genres.append(pk)
        
        result_d = await database.fetch_one(query=models.directors.select().where(models.directors.c.name == movie.director))
        if result_d:
            director_id = result_d.id
        else:
            director_c = models.directors.insert().values({"name":movie.director})
            pk = await database.execute(director_c) 
            director_id = pk
        new_movie = schemas.MovieCreate(name=movie.name, score=movie.imdb_score, director_id=director_id, genres_id=genres)
        await create_movie(new_movie)