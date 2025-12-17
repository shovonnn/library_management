# Testing Guide

## Overview

This guide covers testing strategies and instructions for the Library Management System.

## 🧪 Backend Testing

### Setup Test Environment

```bash
cd server
pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run with verbose output
pytest -v

# Run specific test file
pytest accounts/tests.py

# Run specific test
pytest accounts/tests.py::TestUserModel::test_user_creation
```

### Test Structure

```
server/
├── accounts/
│   ├── tests.py          # User model tests
│   └── test_api.py       # Authentication API tests
└── books/
    ├── tests.py          # Book & Loan model tests
    └── test_api.py       # Books & Loans API tests
```

### Writing Tests

Example test:
```python
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
```

## 🎨 Frontend Testing

### Setup

```bash
cd client
npm install
```

### Running Tests

```bash
# Run tests (when implemented)
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

## 🔄 Integration Testing

### Manual API Testing

#### 1. Authentication Flow

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123!"
  }'

# Save the access token from response
export TOKEN="your_access_token_here"

# Get profile
curl http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer $TOKEN"
```

#### 2. Books API

```bash
# List books
curl http://localhost:8000/api/books/

# Get specific book
curl http://localhost:8000/api/books/1/

# Create book (admin only)
curl -X POST http://localhost:8000/api/books/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Book",
    "author": "Test Author",
    "isbn": "1234567890123",
    "category": "Fiction",
    "page_count": 300,
    "total_copies": 5,
    "available_copies": 5
  }'
```

#### 3. Loans API

```bash
# Borrow a book
curl -X POST http://localhost:8000/api/loans/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1
  }'

# Get my loans
curl http://localhost:8000/api/loans/my-loans/ \
  -H "Authorization: Bearer $TOKEN"

# Return a book
curl -X POST http://localhost:8000/api/loans/1/return/ \
  -H "Authorization: Bearer $TOKEN"
```

### Using Swagger UI

1. Navigate to http://localhost:8000/swagger/
2. Click "Authorize"
3. Enter: `Bearer your_access_token`
4. Try different endpoints interactively

## 🔍 Test Scenarios

### User Journey Tests

#### Scenario 1: New User Registration and First Borrow
1. Navigate to http://localhost:3000
2. Click "Sign Up"
3. Fill registration form
4. Verify redirect to login
5. Login with new credentials
6. Browse books
7. Search for a book
8. Borrow a book
9. Check "My Loans"
10. Verify book appears

#### Scenario 2: Admin Book Management
1. Login as admin
2. Navigate to Admin Panel
3. Add a new book
4. Verify book appears in list
5. Edit the book
6. Verify changes saved
7. Delete the book (optional)

#### Scenario 3: Book Return Flow
1. Login as user with active loan
2. Navigate to "My Loans"
3. Click "Return Book"
4. Verify status changes to "Returned"
5. Check book availability increased

## 🐛 Debugging Tests

### Backend Debugging

```bash
# Run with print statements
pytest -s

# Run with Python debugger
pytest --pdb

# Show all print output
pytest -v -s
```

### Frontend Debugging

```bash
# Run in debug mode
npm run dev

# Check browser console
# Open DevTools (F12)
# Check Console tab for errors
```

## 📊 Coverage Reports

### Backend Coverage

```bash
cd server
pytest --cov --cov-report=html
open htmlcov/index.html
```

### Frontend Coverage

```bash
cd client
npm test -- --coverage
open coverage/lcov-report/index.html
```

## 🔒 Security Testing

### Check for Common Vulnerabilities

```bash
# Backend
cd server
pip install safety
safety check

# Frontend
cd client
npm audit
```

### Test Authentication

- [ ] Verify JWT tokens expire correctly
- [ ] Test token refresh mechanism
- [ ] Verify protected routes require authentication
- [ ] Test password strength requirements
- [ ] Verify logout clears tokens

### Test Authorization

- [ ] Verify regular users cannot access admin endpoints
- [ ] Test that users can only view their own loans
- [ ] Verify book creation requires admin role
- [ ] Test CORS configuration

## 🚀 Performance Testing

### Load Testing with Apache Bench

```bash
# Test books endpoint
ab -n 1000 -c 10 http://localhost:8000/api/books/

# Test with authentication
ab -n 1000 -c 10 -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/loans/my-loans/
```

### Database Query Optimization

```bash
# Enable query logging in settings.py
DEBUG = True
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## ✅ Test Checklist

### Before Deployment

- [ ] All backend tests pass
- [ ] All frontend tests pass
- [ ] Manual testing completed
- [ ] API documentation verified
- [ ] Security tests pass
- [ ] Performance acceptable
- [ ] Error handling works
- [ ] Database migrations work
- [ ] Docker builds successfully
- [ ] Environment variables configured

### User Acceptance Testing

- [ ] User registration works
- [ ] Login/logout works
- [ ] Password change works
- [ ] Book search works
- [ ] Book filtering works
- [ ] Borrowing books works
- [ ] Returning books works
- [ ] Profile updates work
- [ ] Admin can add books
- [ ] Admin can edit books
- [ ] Admin can delete books
- [ ] Responsive design works on mobile
- [ ] All forms validate correctly
- [ ] Error messages display properly

## 🐳 Docker Testing

```bash
# Build and test
docker-compose build
docker-compose up -d
docker-compose exec backend pytest
docker-compose logs

# Clean up
docker-compose down -v
```

## 📱 Mobile Testing

Test on different devices:
- iPhone (Safari)
- Android (Chrome)
- Tablet (iPad)

Test scenarios:
- Navigation menu (hamburger)
- Form inputs (touch-friendly)
- Book cards (tap interactions)
- Responsive layouts

## 🔄 Continuous Integration

Tests automatically run on:
- Every push to main branch
- Every pull request
- See `.github/workflows/ci.yml`

## 📝 Test Data

### Create Test Users

```bash
docker-compose exec backend python manage.py shell
```

```python
from django.contrib.auth import get_user_model
User = get_user_model()

# Regular user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123',
    first_name='Test',
    last_name='User'
)

# Admin user
admin = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='adminpass123'
)
```

### Load Sample Books

```bash
docker-compose exec backend python create_sample_data.py
```

## 🆘 Common Issues

### Tests Failing

1. Check database connection
2. Verify migrations are up to date
3. Check environment variables
4. Clear test database
5. Review test logs

### Frontend Tests Not Running

1. Clear node_modules
2. Reinstall dependencies
3. Check Node version
4. Review package.json scripts

## 📚 Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [React Testing Library](https://testing-library.com/react)
- [API Testing Best Practices](https://testfully.io/blog/api-testing-best-practices/)

---

For questions or issues with testing, please create an issue on GitHub.
