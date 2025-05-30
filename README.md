# TechWizards Backend API - Mexican Restaurant

## Overview
This is the backend API for the Mexican Restaurant application, built with FastAPI and Supabase. It provides authentication, user management, and will support menu and order management.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Supabase account and project

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd techwizards-backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your Supabase credentials
   ```

5. **Set up database:**
   - Run `create_users_table.sql` in your Supabase SQL editor
   - Apply RLS policies from `supabase_rls_policies.sql`

6. **Start the server:**
   ```bash
   ./start.sh
   # OR manually:
   uvicorn main:app --host 127.0.0.1 --port 8001 --reload
   ```

## 🌐 Production Deployment

### Render Deployment
This repository is configured for deployment on Render.

1. **Environment Variables on Render:**
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_API_KEY`: Your Supabase anon key
   - `ENVIRONMENT`: production

2. **Build Command:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Command:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

### Other Platforms
For other hosting platforms, ensure:
- Python 3.8+ runtime
- Install dependencies from `requirements.txt`
- Set environment variables
- Run with: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 📁 Project Structure

```
techwizards-backend/
├── main.py                     # FastAPI application entry point
├── supabase_client.py         # Database client and functions
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create from env.example)
├── env.example               # Environment variables template
├── start.sh                  # Development start script
├── README.md                 # This file
├── create_users_table.sql    # Database schema for users table
├── supabase_rls_policies.sql # Row Level Security policies
├── LOGIN_SETUP_GUIDE.md      # Detailed login system documentation
├── SIGNUP_SETUP_GUIDE.md     # Detailed signup system documentation
├── RLS_SETUP_GUIDE.md        # Database security setup guide
├── SUPABASE_SETUP.md         # Supabase configuration guide
└── archive_old_backend/      # Archived old backend implementation
```

## 🔌 API Endpoints

### Authentication
- `POST /auth/login` - User login with username or email
- `POST /signup` - User registration

### User Management
- `GET /users` - List all users (admin only)

### Health Check
- `GET /health` - API health status

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  full_name TEXT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  phone_number TEXT,
  role TEXT DEFAULT 'customer',
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 🔐 Authentication System

### Features
- ✅ User registration with validation
- ✅ Login with username OR email
- ✅ Role-based authentication (admin, worker, customer)
- ✅ Session management
- ✅ Password validation
- ✅ Duplicate checking

### User Roles
- **Customer**: Default role, access to menu and ordering
- **Worker**: Access to order management
- **Admin**: Full system access

## 🛡️ Security

### Current Implementation
- Input validation on all endpoints
- CORS configuration for frontend integration
- Row Level Security (RLS) policies in Supabase
- Error handling without sensitive data exposure

### Production Recommendations
- [ ] Implement password hashing (bcrypt)
- [ ] Add JWT token authentication
- [ ] Implement rate limiting
- [ ] Add email verification
- [ ] Set up password reset functionality
- [ ] Add two-factor authentication

## 🔧 Configuration

### Environment Variables
Required environment variables:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_API_KEY=your_supabase_anon_key
ENVIRONMENT=production  # or development
```

### CORS Settings
Update `main.py` with your frontend domain:
```python
allow_origins=[
    "http://localhost:3000",  # Local development
    "https://your-frontend-domain.com",  # Your production frontend
]
```

## 🧪 Testing

### Manual Testing
```bash
# Health check
curl https://your-backend-url.com/health

# User registration
curl -X POST https://your-backend-url.com/signup \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "Test User",
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "phoneNumber": "1234567890"
  }'

# User login
curl -X POST https://your-backend-url.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

## 📚 Documentation

- **Setup Guides**: Detailed setup instructions in `*_SETUP_GUIDE.md` files
- **API Documentation**: Available at `/docs` endpoint when server is running
- **Database Schema**: See `create_users_table.sql`

## 🔄 Frontend Integration

This backend is designed to work with the TechWizards Frontend:
- **Frontend Repository**: techwizards-frontend
- **Local Frontend**: `http://localhost:3000`
- **Production Frontend**: Update CORS settings with your domain

## 📝 Development Notes

### Adding New Features
1. Add new functions to `supabase_client.py` for database operations
2. Create new endpoints in `main.py`
3. Update documentation
4. Test thoroughly

### Database Changes
1. Create SQL migration files
2. Update `create_users_table.sql` if needed
3. Update RLS policies if required
4. Document changes

## 🐛 Troubleshooting

### Common Issues
- **Port issues**: Render assigns port automatically via `$PORT`
- **Supabase connection failed**: Check environment variables
- **CORS errors**: Verify frontend URL in CORS settings
- **Database errors**: Check RLS policies and table permissions

### Logs
Check application logs in your hosting platform dashboard.

## 📞 Support

For issues or questions:
1. Check the setup guides in this repository
2. Review the API documentation at `/docs`
3. Check application logs

---

**Status**: ✅ Production Ready
**Last Updated**: May 29, 2025
**Version**: 1.0.0
**Hosting**: Render.com 