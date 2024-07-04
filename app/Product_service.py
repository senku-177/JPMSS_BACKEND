from fastapi import APIRouter,Body
from app.Product import Product
from app.enums import ProductStatus
from app.Product import Product
from app.Product_Cluster import Product_Cluster
from app.Description_gen import generate_description
from app.Category import Category

from app.Query import Query


router = APIRouter()


@router.get("/products")
def get_all_products():
    try:

        products= Product.get_all_active_products()
        return {"details":products}
    except Exception as e:
        return {"error":str(e)}
@router.post("/products")
def add_new_product(product:Product=Body(...)):
    
    if product.name == None:
        return {"error":"Name is required"}
    if product.description == None:
        return {"error":"Description is required"}
    if product.quantity == None:
        return {"error":"Quantity is required"}
    
    product.status = ProductStatus.ACTIVE
    product= product.dict()
    print(product)
    product= Product.add_product(product)

    return product


@router.post("/products_cluster")
def add_new_request(product:Product_Cluster=Body(...)):
    if product.name == None:
        return {"error":"Name is required"}
    if product.quantity == None:
        return {"error":"Quantity is required"}
    if product.images == None:
        return {"error":"Images is required"}
    if product.colors == None:
        return {"error":"Colors is required"}
    if product.category == None:
        return {"error":"Category is required"}
    product.status = ProductStatus.PROGRESS.value
    product = product.dict()


    product = Product.add_product(product)
    return {"details":"query added successfully"}



@router.put("/update_status/{product_sku}")
def update_product_status(product_sku:str, status:ProductStatus):
    
    product = Product.update_status(product_sku,status)
    return {"details":product}

@router.get("/products/{product_sku}")
def get_product(product_sku:str):
    product = Product.get_product_by_sku(product_sku)
    return {"details":product}


@router.put("/products/{product_sku}")
def update_product_api(product_sku:str, product:Product):
    product=product.dict()
    
    product = Product.update_product(sku=product_sku,product=product)
    return {"details":"updated successfully"}

@router.delete("/products/{product_sku}")
def delete_product(product_sku:str):
    product = Product.delete_product(product_sku)
    return {"details":product}

@router.get("/products_unapproved")
def get_unapproved_products_api():
    products = Product.get_unapproved_products()
    return {"details":products}

@router.get("/product_display/{category}")
def get_products_by_categor_api(category:str):
    products = Product.get_products_by_category(category)
    return {"details":products}


@router.post("/product_quantity/{product_sku}")
def update_product_quantity(product_sku:str,quantity:int):
    Product.update_quantity(product_sku,quantity)
    return {"details":"quantity updated successfully"}

@router.post("generate_description")
def generate_description_api(color:str,category:str,description:str):
    try:
        keywords=f"{color},{category},{description}"
        description = generate_description(keywords) 
        return {"details":"description generated successfully"}

    except Exception as e:
        return {"error":str(e)}
    


@router.post("/query_generate")
def generate_query(query:Query=Body(...)):
    query = query.dict()

    Query.create_query(query)
    return {"details":"query generated successfully"}

@router.get("/get_all_queries")
def get_all_queries():
    queries = Query.get_all_queries()
    return {"details":queries}

@router.put("/update_query_status/{query_id}")
def update_query_status(query_id:str,status:str):
    Query.update_status(query_id,status)
    return {"details":"status updated successfully"}

@router.post("/create_category")
def create_category_api(category:str):
    Category.create_category(category)
    return {"details":"category created successfully"}

@router.get("/get_all_categories")
def get_all_categories_api():
    categories = Category.get_all_categories()
    return {"details":categories}

    

@router.get("/get_out_of_stock_products")
def get_all_out_of_stock():

    products = Product.get_all_out_of_stock()
    return {"details":products}







