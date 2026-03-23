from supabase import create_client, Client
from fastapi import HTTPException
from typing import Optional

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise HTTPException(status_code=500, detail="Supabase URL or key is missing")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_supabase() -> Client:
    return supabase

async def get_user_id_from_token(token: str) -> Optional[str]:
    try:
        user_id = await supabase.auth().get_user(token)
        return user_id.get("user_id")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_user_from_id(user_id: str) -> Optional[dict]:
    try:
        user = await supabase.from_("users").select("*").eq("id", user_id).execute()
        return user.data[0] if user.data else None
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")

async def get_todo_from_id(todo_id: str) -> Optional[dict]:
    try:
        todo = await supabase.from_("todos").select("*").eq("id", todo_id).execute()
        return todo.data[0] if todo.data else None
    except Exception as e:
        raise HTTPException(status_code=404, detail="Todo not found")

async def get_todos_from_user_id(user_id: str) -> Optional[list]:
    try:
        todos = await supabase.from_("todos").select("*").eq("user_id", user_id).execute()
        return todos.data if todos.data else []
    except Exception as e:
        raise HTTPException(status_code=404, detail="Todos not found")

async def create_todo(todo: dict) -> Optional[dict]:
    try:
        result = await supabase.from_("todos").insert([todo]).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create todo")

async def update_todo(todo_id: str, todo: dict) -> Optional[dict]:
    try:
        result = await supabase.from_("todos").update(todo).eq("id", todo_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update todo")

async def delete_todo(todo_id: str) -> Optional[dict]:
    try:
        result = await supabase.from_("todos").delete().eq("id", todo_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete todo")