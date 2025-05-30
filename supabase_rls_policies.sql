-- Supabase RLS Policies for login table
-- Run these commands in your Supabase SQL Editor

-- First, ensure the login table exists (if it doesn't already)
CREATE TABLE IF NOT EXISTS login (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security on the login table
ALTER TABLE login ENABLE ROW LEVEL SECURITY;

-- Policy to allow SELECT (read) operations for all users
CREATE POLICY "Allow public read access" ON login
    FOR SELECT
    USING (true);

-- Policy to allow INSERT (create) operations for all users
CREATE POLICY "Allow public insert access" ON login
    FOR INSERT
    WITH CHECK (true);

-- Policy to allow DELETE operations for all users
CREATE POLICY "Allow public delete access" ON login
    FOR DELETE
    USING (true);

-- Policy to allow UPDATE operations for all users (optional, in case you need it later)
CREATE POLICY "Allow public update access" ON login
    FOR UPDATE
    USING (true)
    WITH CHECK (true);

-- Alternative: If you want to disable RLS entirely for testing (less secure)
-- Uncomment the line below instead of using the policies above
-- ALTER TABLE login DISABLE ROW LEVEL SECURITY; 