from pydantic import BaseModel
import uuid

from pymongo import MongoClient
from bson.objectid import ObjectId
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS")

client = MongoClient(MONGO_DETAILS)
database = client["JPM"]
Category_collection = database.get_collection("Category")

class Category(BaseModel):
    name:str
    id: str = str(uuid.uuid4())
    number_of_products:int = 0


    @classmethod
    def create_category(cls,category:str):
        try:
            id = str(uuid.uuid4())
            category = {"name":category,"id":id}
            Category_collection.insert_one(category)
        except Exception as e:
            raise e
        

    @classmethod
    def get_all_categories(cls):
        try:
            categories = Category_collection.find({})
            list=[]
            for category in categories:
                category.pop("_id")
                list.append(category)
            return list
        except Exception as e:
            raise e
        
    @classmethod
    def update_num_products(cls,category_id:str,number_of_products:int):
        try:
            cate=Category_collection.find({"id":category_id})
            cat= cate.get("number_of_products")
            cat+=number_of_products
            Category_collection.update_one({"id":category_id},{"$inc":{"number_of_products":cat}})
        except Exception as e:
            raise e