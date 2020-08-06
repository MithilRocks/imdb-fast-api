from typing import List, Optional, Dict
from pydantic import BaseModel, validator, Field

class MovieBase(BaseModel):
    name: str
    score: float

    @validator('score')
    def check_zero(cls, v):
        if v <= 0:
            raise ValueError(f'Score should be greater than 0')
        elif v > 10:
            raise ValueError(f'Score should be between 0 and 10')
        return v


class Director(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Genre(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class MovieCreate(MovieBase):
    director_id: int
    genres_id: List[int] = []

class Movie(MovieBase):
    id: int
    popularity: float
    director: Director
    genres: List[Genre] = []
    
    class Config:
        orm_mode = True

class MovieUpdate(BaseModel):
    name: Optional[str] = None
    score: Optional[float] = None
    director_id: Optional[int] = None
    genres_id: Optional[List[int]] = None

class MovieUpdateFinal(MovieUpdate):
    id: int

    class Config:
        orm_mode = True

class BulkMovies(BaseModel):
    director: str
    genre: List[str]
    imdb_score: float
    name: str