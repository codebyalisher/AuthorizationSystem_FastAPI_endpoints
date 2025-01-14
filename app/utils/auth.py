from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User
from fastapi.responses import JSONResponse
from app.schemas.auth import UserSignup, UserSignin, UserResponse,TokenData, Token
from app.utils.send_email import send_verification_email
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_SCERET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
REFRESH_TOKEN_SECRET_KEY = os.getenv("REFRESH_TOKEN_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))                                           


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserSignup):

    if user.password != user.confirm_password:

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"status_code":status.HTTP_400_BAD_REQUEST, "message": "Passwords do not match"})
    
    if len(user.password) < 8:

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"status_code":status.HTTP_400_BAD_REQUEST, "message": "Password must be at least 8 characters long"})
    
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"status_code": status.HTTP_400_BAD_REQUEST, "message": "Email already registered"})
      
    hashed_password = pwd_context.hash(user.password)

    if not hashed_password:

        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"status_code":status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "Failed to hash password"})
    
    db_user = User(email=user.email, password=hashed_password)

    db.add(db_user)

    db.commit()

    db.refresh(db_user)    

    send_verification_email(db_user.email)


    return JSONResponse(status_code=status.HTTP_201_CREATED,content={

        "status_code": status.HTTP_201_CREATED,

        "message":"Email verification link sent to Your Email successfully. Please verify your email address.",

        "data": {

            "user": {

                "id": db_user.id,

                "email": db_user.email,

                "is_verified": db_user.is_verified,

                "password": db_user.password

            }

        }

    })


def authenticate_user(db: Session, email: str, password: str):

    if not db:

        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"status_code":status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "Failed to connect to database"})
    
    db_user = db.query(User).filter(User.email ==email).first()
    
    if not db_user:

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"status_code":status.HTTP_404_NOT_FOUND, "message": "User not found"})
    
    if not pwd_context.verify(password, db_user.password):

        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,content={"status_code":staus.HTTP_401_UNAUTHORIZED, "message": "Incorrect password"})
    
    if not db_user.is_verified:

        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,content={"status_code":status.HTTP_403_FORBIDDEN, "message": "Not Authorized"})

    return db_user
    

def create_access_token(data: dict, expires_delta: timedelta):

    payload = data.copy()
    payload["exp"] = datetime.utcnow() + expires_delta
    payload["iat"] = datetime.utcnow()  # Issued at
    payload["sub"] = "access_token"

    return jwt.encode(payload, ACCESS_TOKEN_SCERET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires_delta: timedelta):

    payload = data.copy()

    payload["exp"] =datetime.utcnow() + expires_delta

    return jwt.encode(payload, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, secret_key: str = ACCESS_TOKEN_SCERET_KEY):

    try:

        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])    

        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def create_tokens(user):

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)  # Fixed this

    access_token = create_access_token(data={"user_id": user.id}, expires_delta=access_token_expires)

    refresh_token = create_refresh_token(data={"user_id": user.id}, expires_delta=refresh_token_expires)

    return access_token, refresh_token

