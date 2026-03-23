from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from supabase.py import Database
from typing import List, Optional
from datetime import datetime
from auth import verify_jwt
from schemas.Todo import Todo, TodoCreate, TodoUpdate
from database import supabase_url, supabase_key

router = APIRouter()

supabase: Client = create_client(supabase_url, supabase_key)

class TodoRoute:
    @staticmethod
    @router.get("/todos", response_model=List[Todo])
    async def get_all_todos(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        try:
            payload = verify_jwt(token.credentials)
            user_id = payload.get("user_id")
            todos = await supabase.from_("todos").select("*").eq("user_id", user_id)
            return todos.execute()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    @router.get("/todos/{todo_id}", response_model=Todo)
    async def get_todo(todo_id: int, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        try:
            payload = verify_jwt(token.credentials)
            user_id = payload.get("user_id")
            todo = await supabase.from_("todos").select("*").eq("id", todo_id).eq("user_id", user_id).execute()
            if not todo:
                raise HTTPException(status_code=404, detail="Todo not found")
            return todo[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    @router.post("/todos", response_model=Todo)
    async def create_todo(todo: TodoCreate, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        try:
            payload = verify_jwt(token.credentials)
            user_id = payload.get("user_id")
            new_todo = {
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "due_date": todo.due_date,
                "user_id": user_id
            }
            result = await supabase.from_("todos").insert([new_todo]).execute()
            return result[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    @router.put("/todos/{todo_id}", response_model=Todo)
    async def update_todo(todo_id: int, todo: TodoUpdate, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        try:
            payload = verify_jwt(token.credentials)
            user_id = payload.get("user_id")
            updated_todo = {
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "due_date": todo.due_date
            }
            result = await supabase.from_("todos").update(updated_todo).eq("id", todo_id).eq("user_id", user_id).execute()
            if not result:
                raise HTTPException(status_code=404, detail="Todo not found")
            return result[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    @router.delete("/todos/{todo_id}")
    async def delete_todo(todo_id: int, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        try:
            payload = verify_jwt(token.credentials)
            user_id = payload.get("user_id")
            result = await supabase.from_("todos").delete().eq("id", todo_id).eq("user_id", user_id).execute()
            if not result:
                raise HTTPException(status_code=404, detail="Todo not found")
            return {"message": "Todo deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))