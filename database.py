import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgres://seudlqbpuxrtga:68f2d4d013e20c946bc2dc18d1a9d7c1b3f951d14d72fbc501922d8adc4bf4ea@ec2-54-247-94-127.eu-west-1.compute.amazonaws.com:5432/dcg49t1lfheptp"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

database = databases.Database(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()