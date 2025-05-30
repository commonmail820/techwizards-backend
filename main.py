from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from supabase_client import fetch_login_data, insert_login_data, delete_login_data, update_login_data, signup_user, fetch_users, login_user
import os

print("🚀 Starting Mexican Restaurant API...")
print(f"🌍 Environment: {'Production' if os.getenv('PORT') else 'Development'}")
print(f"🔌 Port: {os.getenv('PORT', '8000')}")

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

# Root endpoint for health checks
@app.get("/")
@app.head("/")
@app.options("/")
async def root():
    return {"message": "Mexican Restaurant API is running", "status": "healthy"}

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
@app.head("/health")
async def health_check():
    return {"status": "healthy"}

# Add additional common health check endpoints
@app.get("/healthz")
@app.head("/healthz")
async def health_check_k8s():
    return {"status": "healthy"}

@app.get("/ping")
@app.head("/ping")
async def ping():
    return {"status": "pong"}

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
