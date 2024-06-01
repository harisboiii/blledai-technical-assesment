# Import necessary modules
from sqlalchemy import create_engine  # For creating the database engine
from sqlalchemy.orm import sessionmaker  # For creating a session factory
from sqlalchemy.ext.declarative import declarative_base  # For creating base class for declarative class definitions

# Define the URL for the SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

# Create the database engine with the SQLite database URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()
