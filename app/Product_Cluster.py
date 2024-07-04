from typing import List
from pydantic import BaseModel
from app.enums import ProductStatus
from typing import Optional

class Product_Cluster(BaseModel):
    name:str
    quantity:int
    images:List[str]
    colors:str
    category: str
    status: Optional[ProductStatus]