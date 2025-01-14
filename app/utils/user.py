from fastapi import HTTPException, Depends,status
from app.schemas.user import UserCreate
from fastapi.responses import JSONResponse
from app.models.user import UserData
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.routes.auth import oauth2_scheme
from dotenv import load_dotenv
from app.utils.auth import verify_token
import os

load_dotenv()


ACCESS_TOKEN_SCERET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    decoded = verify_token(token, ACCESS_TOKEN_SCERET_KEY)
       
    if isinstance(decoded, JSONResponse):
       
        return decoded
    user_id = decoded.get("user_id")
    
    if not user_id:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Invalid token payload"})
            
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found"})
    
    return user

def create_user(user: dict, db: Session):
    user_data = UserData(**user)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data

def get_user_by_id(user_id:id,db:Session):
    user=db.query(UserCreate).filter(UserCreate.id==user_id).first()
    return user

def get_all_users(db:Session):
    users=db.query(UserCreate).all()
    return users

def delete_user(user_id:id,db:Session):
    user=db.query(UserCreate).filter(UserCreate.id==user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return user.id
    
    