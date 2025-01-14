import os
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import UserData,User
from app.schemas.user import CreateUserResponse
from app.utils.user import create_user
from app.utils.imagekit import upload_to_imagekit,delete_image_from_imagekit
from app.database import get_db
from app.utils.user import get_current_user

router = APIRouter(prefix="/data", tags=["users-Detail"])

@router.post("/create-user", response_model=CreateUserResponse)
async def create_users(

    first_name: str = Form(...),

    last_name: str = Form(...),

    db: Session = Depends(get_db),

    file: Optional[UploadFile] = File(None),

    file_url: Optional[str] = Form(None),

    file_path: Optional[str] = Form(None),

    current_user: User = Depends(get_current_user)):
    try:

        if not current_user:

            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found."})
   
        user_data = {
            "user_id": current_user.id,
            "first_name": first_name,
            "last_name": last_name,
            "image_url": None,  
        }              

        upload_result = None
        
        if file:

            upload_result = upload_to_imagekit(file=file.file, file_name="uploaded-image.jpg")
            
        elif file_url:

            upload_result = upload_to_imagekit(file=file_url, file_name="url-image.jpg")           

        elif os.path.exists(file_path):            

            with open(file_path, "rb") as file_obj:

                upload_result = upload_to_imagekit(file=file_obj.read(), file_name="binary-image.jpg")            
        
        else:

            return JSONResponse(status_code=400, content={"message": "No valid input provided for image upload."})

        if upload_result.get("status") != "success":

            return JSONResponse(status_code=400, content={"message": "Image upload failed.", "error": upload_result})

        if upload_result:

            user_data["image_url"] = upload_result["file_id"]

        new_user = create_user(user_data, db)

        new_user_data = {

            "id": new_user.id,

            "first_name": new_user.first_name,

            "last_name": new_user.last_name,

            "image_url": new_user.image_url,

        }

        return JSONResponse(

            status_code=200,

            content={

                "message": "User created successfully.",              

                "data": new_user_data,

            },

        )

    except Exception as e:

        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(e)})


@router.put("/update-user/{user_id}", response_model=CreateUserResponse)
async def update_user(
    user_id: int,
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    file: Optional[UploadFile] = File(None),
    file_url: Optional[str] = Form(None),
    file_path: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)):
    try:
        user_data = db.query(UserData).filter(UserData.id == user_id).first()
        if not user_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found."})

        user = user_data.user 

        upload_result = None
        if file:
            upload_result = upload_to_imagekit(file=file.file, file_name="uploaded-image.jpg")
        elif file_url:
            upload_result = upload_to_imagekit(file=file_url, file_name="url-image.jpg")
        elif os.path.exists(file_path):
            with open(file_path, "rb") as file_obj:
                upload_result = upload_to_imagekit(file=file_obj.read(), file_name="binary-image.jpg")
        else:
            return JSONResponse(status_code=400, content={"message": "No valid input provided for image upload."})

        if upload_result.get("status") != "success":
            return JSONResponse(status_code=400, content={"message": "Image upload failed.", "error": upload_result})

        new_image_id = upload_result["file_id"]
        user_data.image_url = new_image_id

        if first_name:
            user_data.first_name = first_name
        if last_name:
            user_data.last_name = last_name
        if email:
            user.email = email

        db.commit()

        return JSONResponse(
            status_code=200,
            content={
                "message": "User updated successfully.",
                "data": {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user_data.first_name,
                        "last_name": user_data.last_name,
                        "image_url": user_data.image_url,
                    }
                },
            },
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(e)})


@router.get("/get-user-byId/{user_id}", response_model=CreateUserResponse)
async def get_user_byId(
    user_id: int ,  
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    
    try:
        
        user_data = db.query(UserData).filter(UserData.user_id == user_id).first()

        if not user_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found."}) 

        user = user_data.user
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "User data showed successfully.",
                "data": {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user_data.first_name,
                        "last_name": user_data.last_name,
                        "image_url": user_data.image_url,
                    }
                },
            },
        )

    except Exception as e:   

        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(e)})


@router.delete("/delete-user-byId")
async def delete_user_byId(      
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    try:
       
        user_data = db.query(UserData).filter(UserData.user_id == current_user.id).first()

        if not user_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User data not found for the current user."})

        
        if user_data.image_url:
            delete_image_from_imagekit(user_data.image_url)

        db.delete(user_data)
        db.commit()

        return JSONResponse(status_code=200, content={
            "status_code": status.HTTP_200_OK,
            "message": "User data deleted successfully.",
        })

    except Exception as e:   

        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(e)})


@router.get("/get-all-users", response_model=CreateUserResponse)
async def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    try:

        users = db.query(User).join(UserData).filter(User.id == UserData.user_id).all()

        if not users:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No user found."})

        user_list = []
        
        for user in users:
           
            user_list.append({
                "id": user.id,
                "email": user.email, 
                "first_name": user.user_data.first_name,  
                "last_name": user.user_data.last_name,  
                "image_url": user.user_data.image_url,  
            })
            
        return JSONResponse(

            status_code=status.HTTP_200_OK,

            content={

                "message": "Here is the Users Record.",

                "data": {
                    "users": user_list
                },
            },
        )

    except Exception as e:     

        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(e)})