# 🚀 Supabase Database Setup Guide

## 📋 Prerequisites
- You already have a Supabase project set up
- You have access to your Supabase dashboard

## 🔧 Setup Steps

### 1. Get Your Supabase Credentials

Go to your Supabase project dashboard and collect these values:

#### A. Project URL and API Key
- Go to **Settings** → **API**
- Copy your **Project URL** (e.g., `https://your-project.supabase.co`)
- Copy your **anon/public key**

#### B. Database Connection String
- Go to **Settings** → **Database**
- Scroll down to **Connection string**
- Select **URI** tab
- Copy the connection string (it looks like):
  ```
  postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
  ```

### 2. Create Environment File

1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Edit the `.env` file with your actual Supabase credentials:
   ```env
   # Your actual Supabase values
   SUPABASE_URL=https://your-actual-project.supabase.co
   SUPABASE_KEY=your-actual-anon-key
   DATABASE_URL=postgresql://postgres:your-actual-password@db.your-project-ref.supabase.co:5432/postgres
   JWT_SECRET_KEY=your-super-secret-jwt-key
   ENVIRONMENT=development
   ```

### 3. Install PostgreSQL Driver

```bash
pip install psycopg2-binary
```

### 4. Create Database Tables

Run the initialization script to create all necessary tables in your Supabase database:

```bash
python3 init_db.py
```

### 5. Populate with Sample Data (Optional)

If you want to add sample data for testing:

```bash
python3 seed_data.py
```

### 6. Start the Server

```bash
python3 main.py
```

## 🔍 Verification

### Check Database Connection
The server will show a connection message when it starts:
```
🔗 Connecting to database: postgresql://postgres@***
```

### Verify Tables in Supabase
1. Go to your Supabase dashboard
2. Click on **Table Editor**
3. You should see these tables:
   - `users`
   - `menu_items`
   - `menu_categories`
   - `orders`
   - `order_items`

### Test API Endpoints
Run the test script to verify everything works:
```bash
python3 test_api.py
```

## 🛠️ Troubleshooting

### Connection Issues
- **Error: "could not connect to server"**
  - Check your DATABASE_URL is correct
  - Verify your Supabase project is active
  - Check your password in the connection string

### Authentication Issues
- **Error: "password authentication failed"**
  - Verify the password in your DATABASE_URL
  - Make sure you're using the correct database password (not your Supabase account password)

### SSL Issues
- If you get SSL errors, you might need to add `?sslmode=require` to your DATABASE_URL

## 📝 Notes

- The backend will automatically detect if you're using PostgreSQL (Supabase) or SQLite
- If no DATABASE_URL is provided, it falls back to local SQLite for development
- All your data will be stored in your Supabase database
- You can view and manage data through the Supabase dashboard

## 🔄 Next Steps

Once connected to Supabase:
1. Your data persists across server restarts
2. You can scale your database as needed
3. You can use Supabase's real-time features
4. You can manage data through the Supabase dashboard
5. You can set up Row Level Security (RLS) for additional security 