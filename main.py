from typing import List
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.orm import Session

import crud, schemas, models
from database import SessionLocal, engine, database

models.Base.metadata.create_all(engine)

app = FastAPI()

security = HTTPBasic()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# sample hashing
def fake_hash_password(password: str):
    return "hashed" + password

# user authentication
async def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    user = await crud.get_user(credentials.username)
    correct_username = secrets.compare_digest(credentials.username, user.username)
    correct_password = secrets.compare_digest(fake_hash_password(credentials.password), user.password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user.is_admin

@app.get("/movie/{movie_id}", tags=['Main Task Endpoints'], response_model=schemas.Movie)
async def read_movie(movie_id: int, commons: dict = Depends(get_current_username)):
    db_movie = await crud.get_movie(id=movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@app.post("/movie/", tags=['Main Task Endpoints'], response_model=schemas.MovieCreate)
async def create_movie(movie: schemas.MovieCreate, commons: dict = Depends(get_current_username)):
    if not commons:
        raise HTTPException(status_code=401, detail="Access denied")
    db_movie = await crud.get_movie_by_name(name=movie.name)
    if db_movie:
        raise HTTPException(status_code=400, detail="Movie already exists")
    return await crud.create_movie(movie=movie)

@app.put("/movie/", response_model=schemas.MovieUpdateFinal, response_model_exclude_unset=True, tags=['Main Task Endpoints'])
async def update_movie(movie: schemas.MovieUpdateFinal, commons: dict = Depends(get_current_username)):
    if not commons:
        raise HTTPException(status_code=401, detail="Access denied")
    db_movie = await crud.get_movie(id=movie.id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return await crud.update_movie(movie=movie)

@app.delete("/movie/{movie_id}", tags=['Main Task Endpoints'])
async def delete_movie(movie_id: int, commons: dict = Depends(get_current_username)):
    if not commons:
        raise HTTPException(status_code=401, detail="Access denied")
    db_movie = await crud.get_movie(id=movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return await crud.delete_movie(movie_id=movie_id)

@app.get("/directors/", response_model=List[schemas.Director], tags=['Get other info'])
async def get_directors(skip: int = 0, limit: int = 100):
    return await crud.get_directors(skip=skip, limit=limit)

@app.get("/genres/", response_model=List[schemas.Genre], tags=['Get other info'])
async def get_directors(skip: int = 0, limit: int = 100):
    return await crud.get_genres(skip=skip, limit=limit)

@app.post("/bulkmovies/")
async def bulk_movies(movies: List[schemas.BulkMovies]):
    return await crud.bulk_update_movies(movies=movies)
