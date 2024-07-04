from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import uuid
from app.enums import Role
from dotenv import load_dotenv
from pymongo import MongoClient
import os
# Load environment variables
load_dotenv()
MONGO_DETAILS = os.getenv("MONGO_DETAILS")



client = MongoClient(MONGO_DETAILS)
database = client.JPM
users_collection = database.get_collection("users")



class UserCreate(BaseModel):
    name: str
    password: str
    role: Role
    cluster_id: Optional[str]
    phone_number: str

class User(BaseModel):
    id: str = str(uuid.uuid4())
    name: str
    role: Role
    cluster_id: Optional[str]
    phone_number: str

    @classmethod
    async def get_user_by_phone_number(cls, phone_number: str):
        
        try:
            print(MONGO_DETAILS)
            print(users_collection)
            user = users_collection.find_one({"phone_number": phone_number})
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @classmethod
    async def create_user(cls, user_data: UserCreate):
        try:
            new_user = {
                "id": str(uuid.uuid4()),
                "name": user_data.name,
                "password": user_data.password,  # Password should be hashed
                "role": user_data.role,
                "cluster_id": user_data.cluster_id,
                "phone_number": user_data.phone_number
            }
            result =users_collection.insert_one(new_user)
            return new_user if result.inserted_id else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    #login user function
    @classmethod
    async def login(self, phone_number: str, password: str):
        try:
            print(phone_number)
            user = await self.get_user_by_phone_number(phone_number)
            print(user)
            if not user:
                return None  # User with the given phone number not found

            if password == user["password"]:
                return User(
                    id=str(user["id"]),
                    name=user["name"],
                    role=user["role"],
                    cluster_id=user["cluster_id"],
                    phone_number=user["phone_number"]
                )
            else:
                return None  # Incorrect password
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "cluster_id": self.cluster_id,
            "phone_number": self.phone_number
        }

