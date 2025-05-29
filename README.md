# TechWizards Backend

A FastAPI-based backend application for the TechWizards project.

## Project Structure

```
techwizards-backend/
│
├── app/
│   ├── __init__.py          # App package initialization
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration and connection
│   ├── models.py            # SQLAlchemy database models
│   ├── routes/
│   │   └── auth.py          # Authentication routes
│   └── utils.py             # Utility functions
│
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
├── start.sh                 # Startup script
└── README.md               # Project documentation
```

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Authentication**: JWT-based authentication system
- **Database**: SQLAlchemy ORM with SQLite (configurable)
- **Security**: Password hashing with bcrypt
- **Environment Configuration**: Environment-based configuration
- **Auto Documentation**: Swagger UI and ReDoc integration

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd techwizards-backend
```

2. Run the startup script:
```bash
./start.sh
```

Or manually:

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the application:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Access the Application

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/token` - Login and get access token
- `GET /auth/me` - Get current user information

### Root

- `GET /` - Welcome message

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DATABASE_URL=sqlite:///./techwizards.db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
DEBUG=True
HOST=0.0.0.0
PORT=8000

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Development

### Project Structure Explanation

- **app/main.py**: Main FastAPI application with route includes
- **app/database.py**: Database configuration and session management
- **app/models.py**: SQLAlchemy models for database tables
- **app/routes/auth.py**: Authentication-related endpoints
- **app/utils.py**: Helper functions and utilities

### Adding New Routes

1. Create a new file in `app/routes/`
2. Define your router using `APIRouter()`
3. Include the router in `app/main.py`

### Database Migrations

For production use, consider setting up Alembic for database migrations:

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Security Notes

- Change the `SECRET_KEY` in production
- Use a proper database (PostgreSQL, MySQL) in production
- Enable HTTPS in production
- Review and update CORS settings for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
