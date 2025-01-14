from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserInDB(BaseModel):
    id: int
    email: str
    is_verified: bool
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True  # This allows Pydantic to read from ORM objects (SQLAlchemy models)

class UserSignup(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword",
                "confirm_password": "strongpassword"
            }
        }

class UserSignin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    image_url: Optional[str] = None

class UserResponse(BaseModel):
    status: str
    data: dict

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "is_verified": True,
                        "first_name": "John",
                        "last_name": "Doe",
                        "image_url": "https://example.com/image.jpg"
                    }
                }
            }
        }
      
class Token(BaseModel):
    access_token: str
    refresh_token: str  # Add this field
    token_type: str
    
class TokenData(BaseModel):
    email: str | None = None
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str