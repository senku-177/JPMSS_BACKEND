from fastapi import FastAPI
from app.Product_service import router
from app.Auth_service import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, replace with specific origins if needed
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allows all methods, replace with specific methods if needed
    allow_headers=["*"],  # Allows all headers, replace with specific headers if needed
)

app.include_router(router)

app.include_router(router=auth_router)