# Supabase RLS Setup Guide for Login Table

## Steps to Fix RLS Policy Issues

### Option 1: Apply RLS Policies (Recommended)

1. **Go to your Supabase Dashboard**
   - Open your browser and go to [supabase.com](https://supabase.com)
   - Navigate to your project

2. **Open SQL Editor**
   - Click on "SQL Editor" in the left sidebar
   - Click "New Query"

3. **Run the RLS Policies**
   - Copy the contents of `supabase_rls_policies.sql`
   - Paste it into the SQL editor
   - Click "Run" to execute the policies

### Option 2: Disable RLS (For Testing Only)

If you just want to test quickly and don't need security:

1. Go to Supabase SQL Editor
2. Run this single command:
   ```sql
   ALTER TABLE login DISABLE ROW LEVEL SECURITY;
   ```

## Verify the Setup

After applying the policies, test your endpoints:

```bash
# Test GET
curl http://localhost:8001/login

# Test POST
curl -X POST http://localhost:8001/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "123456"}'

# Test GET again (should show the inserted data)
curl http://localhost:8001/login

# Test DELETE
curl -X DELETE http://localhost:8001/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

## What These Policies Do

- **SELECT Policy**: Allows anyone to read data from the login table
- **INSERT Policy**: Allows anyone to insert new records
- **DELETE Policy**: Allows anyone to delete records
- **UPDATE Policy**: Allows anyone to update existing records

## Security Note

These policies allow public access to all operations. In a production environment, you would want more restrictive policies based on user authentication and authorization. 