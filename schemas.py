from typing import List, Optional, Dict
from pydantic import BaseModel, validator, Field

class MovieBase(BaseModel):
    name: str
    score: float


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