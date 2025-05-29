from fastapi import APIRouter
from app.database import supabase
from app.models import SignupData

router = APIRouter()

@router.post("/signup")
def signup(data: SignupData):
    result = supabase.table("users").insert({
        "name": data.name,
        "email": data.email,
        "password": data.password
    }).execute()

    if result.error:
        return {"status": "error", "message": str(result.error)}

    return {"status": "success", "message": "User created"}