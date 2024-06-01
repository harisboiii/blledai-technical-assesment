# Import necessary modules and classes
from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    File,
    UploadFile,
)  # FastAPI components for handling HTTP requests
from fastapi.responses import FileResponse  # For returning file responses
from pydantic import BaseModel, Field  # For defining data models with validation
from sqlalchemy.orm import Session  # For database session management
import models  # Import ORM models
from database import engine, SessionLocal  # Database engine and session management
import auth  # Import authentication router
from CV import face_detection_and_mapping  # Import face detection function
import numpy as np  # Numerical operations
import cv2  # OpenCV for image processing
from tempfile import NamedTemporaryFile

app = FastAPI()
app.include_router(auth.router)

# Will create tables and their values if they don't exist
models.Base.metadata.create_all(bind=engine)


# Session local instance to create our db instance and closing it automatically
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserRequest(BaseModel):
    name: str = Field(min_length=1)


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.post("/")
def create_user(user: UserRequest, db: Session = Depends(get_db)):
    user_model = models.User(name=user.name)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model


@app.put("/{user_id}")
def update_user(user_id: int, user: UserRequest, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.id == user_id).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id}: Does not exist")

    user_model.name = user.name
    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return user_model


@app.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.id == user_id).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} : Does not exist")

    db.delete(user_model)
    db.commit()
    return {"message": f"User ID {user_id} deleted successfully"}


# Endpoint to process an uploaded image
@app.post("/process_image/")
async def process_image(file: UploadFile = File(...)):
    """
    Process an uploaded image by detecting faces and returning the processed image.

    Args:
        file (UploadFile): The uploaded image file.

    Returns:
        FileResponse: The processed image file response.
    """
    try:
        # Read the uploaded image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Call the face detection and processing function
        result_image, cropped_face = face_detection_and_mapping(image)

        # Save the processed image temporarily
        temp_file = NamedTemporaryFile(delete=False, suffix=".jpg")
        cv2.imwrite(temp_file.name, result_image)
        cv2.imwrite(temp_file.name, cropped_face)

        # Return the processed image
        return FileResponse(temp_file.name, media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image processing error: {str(e)}")
