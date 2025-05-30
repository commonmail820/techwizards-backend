import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
LOGIN_TABLE = "login"
USERS_TABLE = "users"

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

async def fetch_login_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{LOGIN_TABLE}?select=*",
            headers=headers
        )
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Status {response.status_code}: {response.text}"}

async def insert_login_data(payload: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/rest/v1/{LOGIN_TABLE}",
            headers=headers,
            json=payload
        )
    
    if response.status_code in [200, 201]:
        try:
            return response.json()
        except:
            return {"success": "Data inserted successfully", "status": response.status_code}
    else:
        return {"error": f"Status {response.status_code}: {response.text}"}

async def delete_login_data(condition: dict):
    # Example: {"email": "test@example.com"}
    query_str = "&".join([f"{key}=eq.{value}" for key, value in condition.items()])
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{SUPABASE_URL}/rest/v1/{LOGIN_TABLE}?{query_str}",
            headers=headers
        )
    
    if response.status_code in [200, 204]:
        try:
            return response.json()
        except:
            return {"success": "Data deleted successfully", "status": response.status_code}
    else:
        return {"error": f"Status {response.status_code}: {response.text}"}

async def update_login_data(condition: dict, payload: dict):
    # Example condition: {"email": "test@example.com"}
    # Example payload: {"password": "newpassword"}
    query_str = "&".join([f"{key}=eq.{value}" for key, value in condition.items()])
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{SUPABASE_URL}/rest/v1/{LOGIN_TABLE}?{query_str}",
            headers=headers,
            json=payload
        )
    
    if response.status_code in [200, 204]:
        try:
            return response.json()
        except:
            return {"success": "Data updated successfully", "status": response.status_code}
    else:
        return {"error": f"Status {response.status_code}: {response.text}"}

async def signup_user(user_data: dict):
    """
    Register a new user with all signup form fields
    Expected fields: fullName, username, email, password, phoneNumber
    """
    # Check if user already exists
    existing_user = await check_user_exists(user_data["email"], user_data["username"])
    if existing_user:
        return {"error": "User with this email or username already exists"}
    
    # Prepare user data for database
    user_payload = {
        "full_name": user_data["fullName"],
        "username": user_data["username"],
        "email": user_data["email"],
        "password": user_data["password"],  # In production, this should be hashed
        "phone_number": user_data["phoneNumber"],
        "role": "customer",  # Default role
        "is_active": True
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/rest/v1/{USERS_TABLE}",
            headers=headers,
            json=user_payload
        )
    
    if response.status_code in [200, 201]:
        try:
            user_result = response.json()
            return {
                "success": "User registered successfully", 
                "status": response.status_code,
                "user": user_result
            }
        except:
            return {
                "success": "User registered successfully", 
                "status": response.status_code
            }
    else:
        return {"error": f"Status {response.status_code}: {response.text}"}

async def check_user_exists(email: str, username: str):
    """
    Check if a user with the given email or username already exists
    """
    async with httpx.AsyncClient() as client:
        # Check email
        email_response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{USERS_TABLE}?email=eq.{email}&select=id",
            headers=headers
        )
        
        # Check username
        username_response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{USERS_TABLE}?username=eq.{username}&select=id",
            headers=headers
        )
    
    if email_response.status_code == 200 and email_response.json():
        return True
    if username_response.status_code == 200 and username_response.json():
        return True
    
    return False

async def fetch_users():
    """
    Fetch all users from the database (for testing purposes)
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{USERS_TABLE}?select=id,full_name,username,email,phone_number,role,is_active,created_at",
            headers=headers
        )
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Status {response.status_code}: {response.text}"}

async def login_user(login_data: dict):
    """
    Authenticate user login by verifying credentials against database
    Expected fields: email/username, password
    """
    email_or_username = login_data.get("email") or login_data.get("username")
    password = login_data.get("password")
    
    if not email_or_username or not password:
        return {"error": "Email/username and password are required"}
    
    # Check if it's an email or username
    if "@" in email_or_username:
        # It's an email
        query_field = "email"
    else:
        # It's a username
        query_field = "username"
    
    async with httpx.AsyncClient() as client:
        # Fetch user by email or username
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{USERS_TABLE}?{query_field}=eq.{email_or_username}&select=*",
            headers=headers
        )
    
    if response.status_code != 200:
        return {"error": f"Database error: {response.status_code}"}
    
    users = response.json()
    
    if not users:
        return {"error": "Invalid email/username or password"}
    
    user = users[0]  # Get the first (and should be only) user
    
    # Verify password (in production, this should use hashed password comparison)
    if user["password"] != password:
        return {"error": "Invalid email/username or password"}
    
    # Check if user is active
    if not user.get("is_active", True):
        return {"error": "Account is deactivated. Please contact support."}
    
    # Return user data (excluding password)
    user_data = {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "phone_number": user["phone_number"],
        "role": user["role"],
        "created_at": user["created_at"]
    }
    
    return {
        "success": "Login successful",
        "user": user_data,
        "token": f"user_{user['id']}_token"  # Simple token for demo (use JWT in production)
    }
