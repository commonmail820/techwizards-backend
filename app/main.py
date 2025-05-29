from fastapi import FastAPI
from app.routes import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS (for frontend interaction)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")