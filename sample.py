from pydantic import BaseModel, validator 
from typing import Optional

class User(BaseModel):
    name: str
    number: Optional[int]

    @validator('number')
    def no_none(cls, v):
        if v is not None:
            return v

obj = User(name='mithil')
print(obj.dict(exclude_unset=True))