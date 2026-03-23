from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from supabase.py import User as SupabaseUser
from jose import jwt
from datetime import datetime, timedelta
from typing import List, Optional
from config import settings
from database import supabase_url, supabase_key
from auth import authenticate_user, get_current_user

router = APIRouter()

class User(BaseModel):
    id: Optional[int]
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

@router.post("/users/")
async def create_user(user: User):
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        data = supabase.auth.sign_up({
            "email": user.username,
            "password": user.password,
        })
        if data.user:
            return UserResponse(id=data.user.id, username=data.user.email)
        else:
            raise HTTPException(status_code=400, detail=data.error.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/me")
async def read_users_me(current_user: SupabaseUser = Depends(get_current_user)):
    return UserResponse(id=current_user.id, username=current_user.email)

@router.get("/users/")
async def read_users(current_user: SupabaseUser = Depends(get_current_user)):
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        data = supabase.from_("users").select("id, email")
        users = [UserResponse(id=user["id"], username=user["email"]) for user in data.execute()]
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))