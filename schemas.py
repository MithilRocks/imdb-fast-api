from typing import List, Optional
from pydantic import BaseModel, validator

class ChemicalBase(BaseModel):
    name: str

class ChemicalCreate(ChemicalBase):
    pass

class Chemical(ChemicalBase):
    id: int

    class Config:
        orm_mode = True

class CommodityBase(BaseModel):
    name: str
    price: Optional[float] = None
    inventory: Optional[float] = None

class CommodityCreate(CommodityBase):
    pass

class Commodity(CommodityBase):
    id: int

    class Config:
        orm_mode = True

class ChemicalCommodityRel(BaseModel):
    chemical_id: int
    percentage: float

    @validator('percentage')
    def check_zero(cls, v):
        if v <= 0:
            raise ValueError(f'percentage should be greater than 0')
        return v

    class Config:
        orm_mode = True