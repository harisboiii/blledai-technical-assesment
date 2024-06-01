# Import necessary modules and classes
from datetime import timedelta, datetime  # For handling date and time
from typing import Annotated  # For type hints
from fastapi import APIRouter, Depends, HTTPException  # FastAPI components
from pydantic import BaseModel  # For defining data models
from sqlalchemy.orm import Session  # For database session management
from starlette import status  # HTTP status codes
from database import SessionLocal  # Local database session
from models import User  # User model
from passlib.context import CryptContext  # For hashing passwords securely
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer  # OAuth2 components
from jose import jwt, JWTError  # For creating and verifying JWT tokens

# Initialize the APIRouter for authentication endpoints
router = APIRouter(
    prefix='/auth',  # URL prefix for these routes
    tags=['auth']  # Tags for API documentation
)

# Constants for JWT token
SECRET_KEY = 'your_secret_key_here'  # Secret key for encoding/decoding JWT tokens
ALGORITHM = 'HS256'  # Algorithm used for encoding JWT tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

# Initialize CryptContext for hashing passwords
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Initialize OAuth2PasswordBearer for token authentication
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

# Pydantic model for creating a new user
class CreateUserRequest(BaseModel):
    username: str
    password: str

# Pydantic model for token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Function to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency annotation for database session
db_dependency = Annotated[Session, Depends(get_db)]

# Function to create an access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoint to create a new user
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    db: db_dependency,
    create_user_request: CreateUserRequest
):
    create_user_model = User(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password),
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return create_user_model

# Endpoint to authenticate and get an access token
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token({'sub': user.username}, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}

# Function to authenticate a user
def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

# Function to create an access token
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
