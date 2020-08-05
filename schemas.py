from typing import List, Optional, Dict
from pydantic import BaseModel, validator, Field

class MovieBase(BaseModel):
    name: str
    score: float


class Director(BaseModel):
    id: int
    name: str

class Genre(BaseModel):
    id: int
    name: str

class MovieCreate(MovieBase):
    director: int
    genres:List[int] = []

class Movie(MovieBase):
    id: int
    director: Director
    genres: List[Genre] = []
    
    class Config:
        orm_mode = True