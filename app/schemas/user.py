from pydantic import BaseModel
from typing import Optional
from .auth import UserResponse

class UserCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    image_url: Optional[str] = None  # Store the image URL    
    class Config:
        orm_mode = True
        

class CreateUserResponse(BaseModel):
    message: str
    data: dict  # This is where we place the user data
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "is_verified": False,
                        "first_name": "John",
                        "last_name": "Doe",
                        "image_url": "https://example.com/image.jpg"
                    }
                }
            }
        }
