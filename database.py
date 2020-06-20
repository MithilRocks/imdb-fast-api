import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql://mithilbhoras:iamapirate@db4free.net/metallics_optim"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

database = databases.Database(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()