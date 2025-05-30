from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from supabase_client import fetch_login_data, insert_login_data, delete_login_data, update_login_data, signup_user, fetch_users, login_user

app = FastAPI(title="Mexican Restaurant API", version="1.0.0")

# CORS middleware for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://your-frontend-domain.com",  # Replace with your actual frontend domain
        "https://techwizards-frontend.onrender.com",  # If using Render
        "*"  # Remove this in production and specify exact domains
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/login")
async def get_logins():
    return await fetch_login_data()

@app.post("/login")
async def create_login(request: Request):
    data = await request.json()
    return await insert_login_data(data)

@app.put("/login")
async def update_login(request: Request):
    data = await request.json()
    condition = {"email": data.get("email")}
    payload = {k: v for k, v in data.items() if k != "email"}
    return await update_login_data(condition, payload)

@app.delete("/login")
async def remove_login(request: Request):
    condition = await request.json()
    return await delete_login_data(condition)

@app.post("/signup")
async def signup(request: Request):
    user_data = await request.json()
    return await signup_user(user_data)

@app.post("/auth/login")
async def login(request: Request):
    login_data = await request.json()
    return await login_user(login_data)

@app.get("/users")
async def get_users():
    return await fetch_users()

# Add a health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
