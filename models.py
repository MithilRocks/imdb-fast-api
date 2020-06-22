from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base

class Element(Base):
    __tablename__ = "elements"

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String(10), unique=True)

class Commodity(Base):
    __tablename__ = "commodities"

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String(255), unique=True)
    price = Column(Float)
    inventory = Column(Float)

class ElementCommodityRelation(Base):
    __tablename__ = "elementcommodityrelation"

    id = Column(Integer, primary_key = True, index=True)
    element_id = Column(Integer, ForeignKey("elements.id"))
    commodity_id = Column(Integer, ForeignKey("commodities.id"))
    percentage = Column(Float)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String(255), unique = True)
    password = Column(String(255))

elements = Element.__table__
commodities = Commodity.__table__
relationships = ElementCommodityRelation.__table__
users = User.__table__
    