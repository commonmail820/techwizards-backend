from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase PostgreSQL database URL
# You'll need to set these environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# If DATABASE_URL is not set, construct it from Supabase credentials
if not DATABASE_URL and SUPABASE_URL:
    # Extract database connection details from Supabase URL
    # Format: postgresql://postgres:[password]@[host]:[port]/postgres
    DATABASE_URL = os.getenv("SUPABASE_DATABASE_URL")

# Fallback to local SQLite for development if no Supabase URL is provided
if not DATABASE_URL:
    print("⚠️  No Supabase DATABASE_URL found. Using local SQLite for development.")
    import tempfile
    DB_DIR = os.path.join(tempfile.gettempdir(), "cafe")
    os.makedirs(DB_DIR, exist_ok=True)
    DB_FILE = os.path.join(DB_DIR, "cafe.db")
    DATABASE_URL = f"sqlite:///{DB_FILE}"

print(f"🔗 Connecting to database: {DATABASE_URL.split('@')[0]}@***" if '@' in DATABASE_URL else DATABASE_URL)

# Create SQLAlchemy engine
if DATABASE_URL.startswith("postgresql"):
    # PostgreSQL configuration for Supabase
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False  # Set to True for SQL debugging
    )
else:
    # SQLite configuration (fallback)
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 