# API Examples

This document provides practical examples for using the Library Management API.

## Table of Contents
- [Authentication](#authentication)
- [User Management](#user-management)
- [Book Management](#book-management)
- [Loan Management](#loan-management)
- [Admin Operations](#admin-operations)
- [Advanced Queries](#advanced-queries)

## Authentication

### Register a New User

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "Alice",
    "last_name": "Johnson",
    "phone_number": "+1234567890",
    "address": "123 Main St, City, Country"
  }'
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Johnson",
    "phone_number": "+1234567890",
    "address": "123 Main St, City, Country",
    "role": "user",
    "date_joined": "2025-12-17T10:00:00Z"
  },
  "message": "User registered successfully. Please login to continue."
}
```

### Login

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "SecurePass123!"
  }'
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

## User Management

### Get User Profile

**Request:**
```bash
curl http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Johnson",
  "phone_number": "+1234567890",
  "address": "123 Main St, City, Country",
  "role": "user",
  "date_joined": "2025-12-17T10:00:00Z"
}
```

### Update Profile

**Request:**
```bash
curl -X PATCH http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alice Updated",
    "phone_number": "+9876543210"
  }'
```

### Change Password

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/change-password/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "SecurePass123!",
    "new_password": "NewSecurePass456!",
    "new_password2": "NewSecurePass456!"
  }'
```

## Book Management

### List All Books (No Authentication Required)

**Request:**
```bash
curl http://localhost:8000/api/books/
```

**Response:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/books/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "isbn": "9780743273565",
      "category": "Fiction",
      "available_copies": 3,
      "total_copies": 5,
      "is_available": true
    }
  ]
}
```

### Get Book Details

**Request:**
```bash
curl http://localhost:8000/api/books/1/
```

**Response:**
```json
{
  "id": 1,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "9780743273565",
  "publisher": "Scribner",
  "publication_date": "1925-04-10",
  "page_count": 180,
  "language": "English",
  "description": "A classic American novel set in the Jazz Age...",
  "category": "Fiction",
  "total_copies": 5,
  "available_copies": 3,
  "cover_image": "https://example.com/cover.jpg",
  "is_available": true,
  "created_at": "2025-12-01T10:00:00Z",
  "updated_at": "2025-12-17T10:00:00Z"
}
```

### Create a Book (Admin Only)

**Request:**
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "1984",
    "author": "George Orwell",
    "isbn": "9780451524935",
    "publisher": "Signet Classic",
    "publication_date": "1949-06-08",
    "page_count": 328,
    "language": "English",
    "description": "A dystopian social science fiction novel...",
    "category": "Science Fiction",
    "total_copies": 10,
    "available_copies": 10
  }'
```

### Update a Book (Admin Only)

**Request:**
```bash
curl -X PATCH http://localhost:8000/api/books/1/ \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "available_copies": 4,
    "description": "Updated description..."
  }'
```

### Delete a Book (Admin Only)

**Request:**
```bash
curl -X DELETE http://localhost:8000/api/books/1/ \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

### Search Books

**Request:**
```bash
curl "http://localhost:8000/api/books/search/?q=gatsby" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565",
    "category": "Fiction",
    "available_copies": 3,
    "total_copies": 5,
    "is_available": true
  }
]
```

## Loan Management

### Borrow a Book

**Request:**
```bash
curl -X POST http://localhost:8000/api/loans/borrow/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"book_id": 1}'
```

**Response:**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com"
  },
  "book": {
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald"
  },
  "borrowed_date": "2025-12-17T10:00:00Z",
  "due_date": "2025-12-31T10:00:00Z",
  "return_date": null,
  "status": "active",
  "is_overdue": false,
  "days_overdue": 0
}
```

### Return a Book

**Request:**
```bash
curl -X POST http://localhost:8000/api/loans/return/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "loan_id": 1,
    "notes": "Book returned in excellent condition"
  }'
```

**Response:**
```json
{
  "message": "Book returned successfully.",
  "loan": {
    "id": 1,
    "status": "returned",
    "return_date": "2025-12-20T10:00:00Z"
  }
}
```

### View My Loans

**Request:**
```bash
curl http://localhost:8000/api/loans/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user_username": "alice",
      "book_title": "The Great Gatsby",
      "borrowed_date": "2025-12-17T10:00:00Z",
      "due_date": "2025-12-31T10:00:00Z",
      "return_date": null,
      "status": "active",
      "is_overdue": false
    }
  ]
}
```

## Admin Operations

### View All Users (Admin Only)

**Request:**
```bash
curl http://localhost:8000/api/auth/users/ \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

### Update User (Admin Only)

**Request:**
```bash
curl -X PATCH http://localhost:8000/api/auth/users/2/ \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "admin",
    "is_active": true
  }'
```

### View All Loans (Admin Only)

**Request:**
```bash
curl http://localhost:8000/api/admin/loans/ \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

### View Overdue Loans (Admin Only)

**Request:**
```bash
curl http://localhost:8000/api/admin/loans/overdue/ \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 5,
    "user_username": "bob",
    "book_title": "To Kill a Mockingbird",
    "borrowed_date": "2025-11-01T10:00:00Z",
    "due_date": "2025-11-15T10:00:00Z",
    "return_date": null,
    "status": "overdue",
    "is_overdue": true
  }
]
```

## Advanced Queries

### Filter Books by Category

```bash
curl "http://localhost:8000/api/books/?category=Fiction"
```

### Filter Available Books

```bash
curl "http://localhost:8000/api/books/?available=true"
```

### Filter Books by Author

```bash
curl "http://localhost:8000/api/books/?author=Fitzgerald"
```

### Filter Books by Page Count Range

```bash
curl "http://localhost:8000/api/books/?min_pages=100&max_pages=500"
```

### Combine Multiple Filters

```bash
curl "http://localhost:8000/api/books/?category=Fiction&available=true&author=Orwell"
```

### Pagination

```bash
# First page (default page size: 10)
curl "http://localhost:8000/api/books/"

# Second page
curl "http://localhost:8000/api/books/?page=2"

# Custom page size
curl "http://localhost:8000/api/books/?page_size=20"
```

### Filter Loans by Status

```bash
curl "http://localhost:8000/api/admin/loans/?status=active" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

### Filter Loans by Date Range

```bash
curl "http://localhost:8000/api/admin/loans/?borrowed_after=2025-12-01&borrowed_before=2025-12-31" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

## Using Python Requests

Here's how to use the API with Python:

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# Register
response = requests.post(f"{BASE_URL}/api/auth/register/", json={
    "username": "alice",
    "email": "alice@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
})
print(response.json())

# Login
response = requests.post(f"{BASE_URL}/api/auth/login/", json={
    "username": "alice",
    "password": "SecurePass123!"
})
tokens = response.json()
access_token = tokens["access"]

# Set authorization header
headers = {"Authorization": f"Bearer {access_token}"}

# List books
response = requests.get(f"{BASE_URL}/api/books/", headers=headers)
print(response.json())

# Borrow a book
response = requests.post(
    f"{BASE_URL}/api/loans/borrow/",
    headers=headers,
    json={"book_id": 1}
)
print(response.json())
```

## Using JavaScript/Fetch

```javascript
const BASE_URL = 'http://localhost:8000';

// Login
async function login(username, password) {
  const response = await fetch(`${BASE_URL}/api/auth/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  const data = await response.json();
  return data.access;
}

// Get books
async function getBooks(accessToken) {
  const response = await fetch(`${BASE_URL}/api/books/`, {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  });
  return await response.json();
}

// Borrow book
async function borrowBook(accessToken, bookId) {
  const response = await fetch(`${BASE_URL}/api/loans/borrow/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ book_id: bookId })
  });
  return await response.json();
}

// Usage
(async () => {
  const token = await login('alice', 'SecurePass123!');
  const books = await getBooks(token);
  console.log(books);
})();
```
