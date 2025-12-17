# Quick Start Guide

## Getting Started in 5 Minutes

### Option 1: Docker (Recommended)

1. **Start the application**
   ```bash
   docker-compose up
   ```

2. **Initialize database (first time only)**
   ```bash
   docker-compose exec web bash init_db.sh
   ```

3. **Access the application**
   - API: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - Docs: http://localhost:8000/swagger

   **Default admin credentials:**
   - Username: `admin`
   - Password: `admin123`

### Option 2: Local Development

1. **Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

2. **Configure database**
   - Edit `.env` file with your PostgreSQL credentials
   - Or use SQLite by setting `DB_ENGINE=django.db.backends.sqlite3`

3. **Initialize**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

## Testing the API

### 1. Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "password2": "TestPass123!"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "TestPass123!"}'
```

Save the `access` token from the response.

### 3. Browse Books (No auth required)
```bash
curl http://localhost:8000/api/books/
```

### 4. Create a Book (Admin only)

Login as admin first:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Then create a book:
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565",
    "page_count": 180,
    "category": "Fiction",
    "total_copies": 5,
    "available_copies": 5
  }'
```

### 5. Borrow a Book
```bash
curl -X POST http://localhost:8000/api/loans/borrow/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"book_id": 1}'
```

### 6. View Your Loans
```bash
curl http://localhost:8000/api/loans/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 7. Return a Book
```bash
curl -X POST http://localhost:8000/api/loans/return/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"loan_id": 1}'
```

## Using the Interactive API Documentation

Visit http://localhost:8000/swagger/ for interactive API documentation where you can:
1. Click "Authorize" button
2. Enter: `Bearer YOUR_ACCESS_TOKEN`
3. Try out any endpoint directly from the browser

## Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Common Issues

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Database connection error
- Check PostgreSQL is running
- Verify credentials in `.env`
- Or use SQLite for quick testing

### Permission denied on init_db.sh
```bash
chmod +x init_db.sh
```

## Next Steps

- Explore the admin panel at http://localhost:8000/admin
- Read the full API documentation at http://localhost:8000/swagger
- Check out the main README.md for detailed information
- Run tests to ensure everything works: `pytest`
