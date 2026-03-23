from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from supabase.py import Auth
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Initialize Supabase client
supabase_url: str = SUPABASE_URL
supabase_key: str = SUPABASE_KEY
supabase: Client = create_client(supabase_url, supabase_key)

# Initialize FastAPI app
app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",
    "https://todo-app.example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication
from auth import authenticate_user, create_access_token

# Routes
from routes.User import user_router
from routes.Todo import todo_router

app.include_router(user_router)
app.include_router(todo_router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Todo App"}

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

# 404 error handling
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=404, content={"error": "Not Found"})

# 500 error handling
@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

# JWT token verification
async def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await authenticate_user(username=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Token data model
class TokenData(BaseModel):
    username: str | None = None

# Credentials exception
credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# Token expiration exception
token_expired_exception = HTTPException(
    status_code=401,
    detail="Token has expired",
    headers={"WWW-Authenticate": "Bearer"},
)