from fastapi import APIRouter, FastAPI,Body, HTTPException
from app.User import User, UserCreate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router= APIRouter(prefix="/auth")

@router.post("/register",status_code=201)
async def register_user(user: UserCreate = Body(...)):
    try:
        if user.phone_number is None:
            raise HTTPException(status_code=400, detail="Phone number not present")

        existing_user = await User.get_user_by_phone_number(str(user.phone_number))
        print(existing_user)
        if existing_user:
            raise HTTPException(status_code=400, detail="Phone number already exists")
        print("here")
        user_obj = await User.create_user(user)
        print(user_obj)
        if not user_obj:
            raise HTTPException(status_code=500, detail="User creation failed")

        return {"details": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login_user(phone_number: str, password: str):
    try:
        user_obj = await User.login(phone_number=phone_number,password=password)
        if not user_obj:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return user_obj
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
