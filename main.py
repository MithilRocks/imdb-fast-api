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

@app.get("/movie/{movie_id}", response_model=schemas.Movie)
async def read_movie(movie_id: int):
    db_movie = await crud.get_movie(id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@app.post("/movies/")
async def create_movie(movie: schemas.MovieCreate):
    db_movie = await crud.get_movie_by_name(name=movie.name)
    if db_movie:
        raise HTTPException(status_code=400, detail="Movie already exists")
    return await crud.create_movie(movie=movie)

""" 
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
    return credentials.username

# including elements router
app.include_router(
    elements.router,
    prefix="/element",
    responses={404: {"description":"api not found"}},
    dependencies=[Depends(get_current_username)]
)

# including commodities router
app.include_router(
    commodities.router,
    prefix="/commodity",
    responses={404: {"description":"api not found"}},
    dependencies=[Depends(get_current_username)]
) """