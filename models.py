# Import necessary modules
from sqlalchemy import Column, Integer, String  # For defining table columns
from database import Base  # Import the declarative base class

# Define a User class that inherits from the declarative base class
class User(Base):
    # Define the table name for this model
    __tablename__ = "users"

    # Define columns for the users table
    id = Column(Integer, primary_key=True, index=True)  # Primary key column for unique identification
    username = Column(String, unique=True, index=True)  # Column for storing usernames (unique)
    hashed_password = Column(String)  # Column for storing hashed passwords
