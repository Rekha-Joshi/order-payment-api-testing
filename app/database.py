# This file sets up the PostgreSQL connection, session factory, and base class for ORM models.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg://localhost/order_payment_db" #tells Python which DB to connect to

engine = create_engine(DATABASE_URL) #creates DB connection engine
SessionLocal = sessionmaker(bind=engine) #used later to talk to DB
Base = declarative_base() #base class for ORM models