from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base

class Chemical(Base):
    __tablename__ = "chemicals"

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String(10), unique=True)

class Commodity(Base):
    __tablename__ = "commodities"

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String(255), unique=True)
    price = Column(Float)
    inventory = Column(Float)

class ChemicalCommodityRelation(Base):
    __tablename__ = "chemicalcommodityrelation"

    id = Column(Integer, primary_key = True, index=True)
    chemical_id = Column(Integer, ForeignKey("chemicals.id"))
    commodity_id = Column(Integer, ForeignKey("commodities.id"))
    percentage = Column(Float)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String(255), unique = True)
    password = Column(String(255))

chemicals = Chemical.__table__
commodities = Commodity.__table__
relationships = ChemicalCommodityRelation.__table__
users = User.__table__
    