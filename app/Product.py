from pydantic import BaseModel
from typing import List, Optional
from app.enums import ProductStatus
from app.Category import Category
import random

from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS")

client = MongoClient(MONGO_DETAILS)
database = client["JPM"]
product_collection = database.get_collection("products")


class Product(BaseModel):
    name:str
    description:Optional[str]
    quantity:int
    price:Optional[float]
    weight:Optional[float]
    images:List[str]
    colors:str
    SKU:Optional[str]
    category: str
    status: ProductStatus

   
    def to_dict(cls):
        return {
            "name": cls.name,
            "description": cls.description if cls.description !=None else "" ,
            "quantity": cls.quantity,
            "price": cls.price if cls.price !=None else 0.0,
            "weight": cls.weight if cls.weight !=None else 0.0,
            "images": cls.images,
            "colors": cls.colors,
            "SKU": cls.SKU if cls.SKU !=None else "",
            "category": cls.category,
            "status": cls.status.value
            }
    @staticmethod
    def get_all_active_products():
        try:
            # Query MongoDB collection for products with active status
            list=[]
            for product in product_collection.find({}):
                print(type(product))
                if product["status"] == ProductStatus.ACTIVE.value:
                    product.pop("_id")  
                    print(product)
                    list.append(product)
            print(list)
            # Convert cursor to list of dictionaries
            
            
            return list
        except Exception as e:
            # Handle exceptions (e.g., logging, returning error response)
            raise e
    @classmethod
    def add_product(cls,product_dict:dict):
        try:
            print(type(product_dict))
            
            product_dict["SKU"] = Product.generate_sku(product_dict.get("name"), product_dict.get("category"))
            
            product=Product(**product_dict)
            product_dict = product.dict()
            product_dict["category"] = product.category
            product_dict["status"] = product.status.value
            print(product_dict)
            insert_result = product_collection.insert_one(product_dict)
            
            return product
        except Exception as e:
            raise e
    @classmethod
    def update_product(sku:str, product:dict):

        product_collection.update_one({"SKU":sku},{"$set":product})
        return product.to_dict()

    @classmethod
    def generate_sku(cls,name: str, category: str):
        print(name,category)
    # Take the first two characters of the category name and product name
        category_code = category[:2].upper()
        name_code = name[:2].upper()

        # Generate a unique 6-digit number
        unique_number = f"{random.randint(0, 999999):06}"

        # Create the SKU
        sku = f"JPM{category_code}{name_code}_{unique_number}"
        return sku
    
    @classmethod
    def get_product_by_sku(cls, sku: str):
        try:
            product = product_collection.find_one({"SKU": sku})
            product.pop("_id")
            return product
        except Exception as e:
            raise e
        



    @classmethod
    def update_status(cls, sku: str, status: ProductStatus):
        try:
            product_collection.update_one({"SKU": sku}, {"$set": {"status": status.value}})
            return {"SKU": sku, "status": status.value}
        except Exception as e:
            raise e
    @classmethod
    def update_product(cls,sku:str,product:dict):
        try:
            print(product)
            product["category"]=product["category"]
            product["status"]=product["status"].value
            product=product_collection.update_one({"SKU":sku},{"$set":product})
            
            
        except Exception as e:
            raise e
    @classmethod 
    def delete_product(cls,sku:str):
        try:
            product=product_collection.delete_one({"SKU":sku})
            return {"details":"product deleted successfully"}
        except Exception as e:
            raise e
    @classmethod
    def get_unapproved_products(cls):
        try:
            list=[]
            for product in product_collection.find({}):
                print(product)
                if product.get("status") == ProductStatus.PROGRESS.value:
                    product.pop("_id")
                    list.append(product)
            return list
            
        except Exception as e:
            raise e
    

    @classmethod
    def get_products_by_category(cls,category:str):
        try:
            list=[]
            for product in product_collection.find({}):
                if product.get("category") == category:
                    product.pop("_id")
                    list.append(product)
            return list
        except Exception as e:
            raise e

    @classmethod
    def update_quantity(cls,sku:str,quantity:int):
        try:
            product_collection.update_one({"SKU":sku},{"$set":{"quantity":quantity}})
            if quantity == 0:
                product_collection.update_one({"SKU":sku},{"$set":{"status":ProductStatus.OUT_OF_STOCK.value}})
                category = product_collection.find_one({"SKU":sku}).get("category")
                Category.update_num_products(category,quantity)
                return {"details":"quantity updated successfully"}

            else:
                product_collection.update_one({"SKU":sku},{"$set":{"status":ProductStatus.ACTIVE.value}})
            return {"details":"quantity updated successfully"}
        except Exception as e:
            raise e
        
    @classmethod
    def get_all_out_of_stock(cls):
        try:
            list=[]
            for product in product_collection.find({}):
                if product.get("status") == ProductStatus.OUT_OF_STOCK.value:
                    product.pop("_id")
                    list.append(product)
            return list
        except Exception as e:
            raise e


