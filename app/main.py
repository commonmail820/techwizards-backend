from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import os

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Request model for signup
class SignupRequest(BaseModel):
    full_name: str
    username: str
    email: str
    password: str
    phone_number: str = None  # Optional field

@app.post("/api/signup")
def signup(user: SignupRequest):
    try:
        response = supabase.table("users").insert({
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "phone_number": user.phone_number
        }).execute()

        return {"message": "User created successfully", "data": response.data}

    except Exception as e:
        print("Signup error:", e)
        raise HTTPException(status_code=500, detail=str(e))