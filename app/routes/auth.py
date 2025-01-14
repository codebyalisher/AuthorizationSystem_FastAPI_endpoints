from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserSignup, UserSignin, UserResponse, UserInDB, Token, TokenData, RefreshTokenRequest
from app.utils.auth import create_user, authenticate_user, create_tokens, verify_token,create_access_token
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_SECRET_KEY = os.getenv("REFRESH_TOKEN_SECRET_KEY")
ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=UserResponse)
def signup(user: UserSignup, db: Session = Depends(get_db)):
    return create_user(db, user)
  

@router.get("/verify", response_model=UserResponse)
def verify_email(email: str = Query(..., description="Email to verify"),db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status_code":status.HTTP_404_NOT_FOUND, "message": "User not found"})
    
    user.is_verified = True

    db.commit()

    db.refresh(user)    

    user_data = UserInDB.from_orm(user)

    return JSONResponse(status_code=status.HTTP_200_OK,content={"status_code":status.HTTP_200_OK,"message":"Email verified successfully", "data": {"user": user_data.dict()}})


@router.post("/signin", response_model=Token)
def signin(response: Response,user: UserSignin,db: Session = Depends(get_db)):

    db_user = authenticate_user(db, user.email, user.password)

    if not db_user:

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"status_code": status.HTTP_401_UNAUTHORIZED, "message": "Invalid email or password"}
            )

    access_token, refresh_token = create_tokens(db_user)

    response.set_cookie(

        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Fixed max_age
        secure=True,  # Use HTTPS in production
        samesite="lax")

    db_user.refresh_token = refresh_token
    db.commit()    
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status_code": status.HTTP_200_OK,
            "message": "Signin Tokens created successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,            
            "data": {
            "user_id" :db_user.id,
            "user_email" :db_user.email,
            },

        },

    )


@router.post("/refresh-token")
def refresh_token(refresh_token: str):
    try:

        decoded = verify_token(refresh_token, REFRESH_TOKEN_SECRET_KEY)

        user_id = decoded.get("user_id")

        if not user_id:
            
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status_code": status.HTTP_401_UNAUTHORIZED, "message": "Invalid token payload"})
            
        new_access_token = create_access_token( {"user_id": user_id}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

        return JSONResponse(status_code=status.HTTP_200_OK,content={"status_code":status.HTTP_200_OK,"message":"new access Token Created Successuflly","new_accessToken_using_refresh_token_": new_access_token})

    except Exception as e:       

        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"status_code":status.HTTP_500_INTERNAL_SERVER_ERROR,"message":"Unexpected error"})


@router.get("/me",response_model=UserResponse)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):        
    
    try:
        decoded = verify_token(token, ACCESS_TOKEN_SECRET_KEY)
        user_id = decoded.get("user_id")
        
        if not user_id:  
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,content={"status_code":status.HTTP_401_UNAUTHORIZED,"message":"Invalid token payload"})
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"status_code":status.HTTP_404_NOT_FOUND,"message":"User not found"})
    
        return JSONResponse(status_code=status.HTTP_200_OK,content={
            "status_code": status.HTTP_200_OK,
            "message": "User details",
            "data": {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "is_verified": user.is_verified,
                }
            }
        })
        
    except:
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Internal server error",                
            },
        )
