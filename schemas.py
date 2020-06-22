from typing import List, Optional, Dict
from pydantic import BaseModel, validator, Field

class ElementBase(BaseModel):
    name: str

class ElementCreate(ElementBase):
    pass

class Element(ElementBase):
    id: int

    class Config:
        orm_mode = True

class CommodityBase(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    inventory: Optional[float] = None

class CommodityCreate(CommodityBase):
    pass

class Commodity(CommodityBase):
    id: int

    class Config:
        orm_mode = True

class ElementCommodityRel(BaseModel):
    element_id: int
    percentage: float

    @validator('percentage')
    def check_zero(cls, v):
        if v <= 0:
            raise ValueError(f'percentage should be greater than 0')
        return v

    class Config:
        orm_mode = True

class CompositionElement(BaseModel):
    element: Element
    percentage: float

    class Config:
        orm_mode = True

class CommodityResponse(Commodity):
    chemical_composition: List[CompositionElement]

    class Config:
        orm_mode = True

class DeleteElement(BaseModel):
    commodity_id: int
    element_id: int

class AddElement(DeleteElement):
    percentage: float

    class Config:
        orm_mode = True