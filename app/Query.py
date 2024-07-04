from typing import List
from pydantic import BaseModel
from pymongo import MongoClient
from bson.objectid import ObjectId
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS")

client = MongoClient(MONGO_DETAILS)
database = client["JPM"]
Query_collection = database.get_collection("query")

class CartProducts(BaseModel):
    SKU:str
    quantity:int

class Query(BaseModel):
    id: str = str(uuid.uuid4())
    name:str
    email:str
    phone:str
    address:str
    Additional_info:str
    products:List[CartProducts]
    status:str = "Pending"



    @classmethod
    def create_query(cls, Query:dict):
        try:
            query = Query_collection.insert_one(Query)
        except Exception as e:
            return {"error":str(e)}
    
    @classmethod
    def get_all_queries(cls):
        try:
            queries = Query_collection.find({})
            list=[]
            for query in queries:
                print(query)
                query.pop("_id")
            list.append(query)

            return list
        except Exception as e:
            return {"error":str(e)}
    @classmethod
    def update_status(cls,query_id:str,status:str):
        try:
            Query_collection.update_one({"id":query_id},{"$set":{"status":status}})

        except Exception as e:
            return {"error":str(e)}
    
    