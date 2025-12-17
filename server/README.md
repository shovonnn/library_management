# Library Management System API

A comprehensive Django REST Framework application for managing a library system with user authentication, book management, and loan tracking.

## 🚀 Features

- **User Management**
  - User registration and authentication (JWT)
  - Role-based access control (Regular Users and Administrators)
  - User profile management
  - Password change functionality

- **Book Management**
  - Browse books (anonymous users)
  - Search books by title, author, ISBN, category
  - Advanced filtering and pagination
  - Add/Edit/Delete books (admin only)
  - Track book availability

- **Loan System**
  - Borrow and return books
  - Automatic due date calculation (14 days)
  - Overdue tracking
  - Loan history
  - Prevent duplicate active loans

- **Admin Panel**
  - Django admin interface for managing users, books, and loans
  - View all loans and overdue items
  - User management

- **Security**
  - JWT authentication
  - Password validation
  - Protection against CSRF, XSS, SQL Injection
  - Secure headers and settings

- **API Documentation**
  - Interactive Swagger UI
  - ReDoc documentation
  - Comprehensive endpoint descriptions

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional)
- Git

## 🛠️ Installation

### Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd library_mgmt
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env file with your configuration
```

5. **Set up PostgreSQL database**
```bash
# Create database
createdb library_db

# Or using psql
psql -U postgres
CREATE DATABASE library_db;
\q
```

6. **Run migrations**
```bash
python manage.py migrate
```

7. **Create superuser**
```bash
python manage.py createsuperuser
```

8. **Run development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

### Docker Setup

1. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

2. **Initialize database (first time only)**
```bash
docker-compose exec web bash init_db.sh
```

3. **Access the application**
- API: `http://localhost:8000`
- Admin Panel: `http://localhost:8000/admin`
- API Documentation: `http://localhost:8000/swagger`

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login and get JWT tokens | No |
| POST | `/api/auth/token/refresh/` | Refresh access token | No |
| GET | `/api/auth/profile/` | Get user profile | Yes |
| PATCH | `/api/auth/profile/` | Update user profile | Yes |
| POST | `/api/auth/change-password/` | Change password | Yes |

### Books

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/books/` | List all books | No |
| POST | `/api/books/` | Create new book | Admin |
| GET | `/api/books/{id}/` | Get book details | No |
| PUT | `/api/books/{id}/` | Update book | Admin |
| DELETE | `/api/books/{id}/` | Delete book | Admin |
| GET | `/api/books/search/?q=query` | Search books | Yes |

### Loans

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/loans/` | Get user's loans | Yes |
| POST | `/api/loans/borrow/` | Borrow a book | Yes |
| POST | `/api/loans/return/` | Return a book | Yes |
| GET | `/api/admin/loans/` | Get all loans | Admin |
| GET | `/api/admin/loans/overdue/` | Get overdue loans | Admin |
| GET | `/api/admin/loans/{id}/` | Get loan details | Admin |

### Admin - User Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/auth/users/` | List all users | Admin |
| GET | `/api/auth/users/{id}/` | Get user details | Admin |
| PATCH | `/api/auth/users/{id}/` | Update user | Admin |
| DELETE | `/api/auth/users/{id}/` | Deactivate user | Admin |

### Documentation

| Endpoint | Description |
|----------|-------------|
| `/swagger/` | Swagger UI documentation |
| `/redoc/` | ReDoc documentation |

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Getting Tokens

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

Response:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using Tokens

Include the access token in the Authorization header:

```bash
curl -X GET http://localhost:8000/api/books/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

## 📖 Usage Examples

### Register a new user

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Search for books

```bash
curl -X GET "http://localhost:8000/api/books/search/?q=python" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Borrow a book

```bash
curl -X POST http://localhost:8000/api/loans/borrow/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"book_id": 1}'
```

### Return a book

```bash
curl -X POST http://localhost:8000/api/loans/return/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"loan_id": 1, "notes": "Book in good condition"}'
```

### Filter books

```bash
# Filter by category
curl -X GET "http://localhost:8000/api/books/?category=Fiction"

# Filter available books
curl -X GET "http://localhost:8000/api/books/?available=true"

# Filter by author
curl -X GET "http://localhost:8000/api/books/?author=Tolkien"

# Combine filters
curl -X GET "http://localhost:8000/api/books/?category=Fiction&available=true"
```

## 🧪 Testing

### Run all tests

```bash
pytest
```

### Run with coverage

```bash
pytest --cov=. --cov-report=html
```

### Run specific test file

```bash
pytest accounts/tests.py
pytest books/test_api.py
```

### View coverage report

```bash
open htmlcov/index.html
```

## 🚀 Deployment

### Heroku Deployment

1. **Install Heroku CLI**
```bash
brew install heroku/brew/heroku  # macOS
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku app**
```bash
heroku create your-app-name
```

4. **Add PostgreSQL addon**
```bash
heroku addons:create heroku-postgresql:mini
```

5. **Set environment variables**
```bash
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
```

6. **Deploy**
```bash
git push heroku main
```

7. **Run migrations**
```bash
heroku run python manage.py migrate
```

8. **Create superuser**
```bash
heroku run python manage.py createsuperuser
```

### Docker Deployment

1. **Build image**
```bash
docker build -t library-management .
```

2. **Run container**
```bash
docker run -p 8000:8000 \
  -e SECRET_KEY="your-secret-key" \
  -e DB_ENGINE="django.db.backends.postgresql" \
  -e DB_NAME="library_db" \
  -e DB_USER="postgres" \
  -e DB_PASSWORD="postgres" \
  -e DB_HOST="host.docker.internal" \
  -e DB_PORT="5432" \
  library-management
```

## 🗄️ Database Schema

### User Model
- username, email, password (hashed)
- first_name, last_name, phone_number, address
- role (user/admin)
- is_active, date_joined

### Book Model
- title, author, isbn (unique)
- publisher, publication_date
- page_count, language, category
- description, cover_image
- total_copies, available_copies
- created_at, updated_at

### Loan Model
- user (FK to User)
- book (FK to Book)
- borrowed_date, due_date, return_date
- status (active/returned/overdue)
- notes

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Django's built-in password hashing
- **Password Validation**: Strong password requirements
- **CSRF Protection**: Django CSRF middleware
- **SQL Injection Prevention**: Django ORM parameterized queries
- **XSS Protection**: Secure headers and content type sniffing prevention
- **HTTPS Ready**: Secure cookie settings for production
- **Rate Limiting**: Can be added with Django REST Framework throttling

## 📦 Project Structure

```
library_mgmt/
├── accounts/               # User authentication and management
│   ├── models.py          # Custom User model
│   ├── serializers.py     # User serializers
│   ├── views.py           # Authentication views
│   ├── permissions.py     # Custom permissions
│   ├── tests.py           # Model tests
│   └── test_api.py        # API tests
├── books/                 # Book and loan management
│   ├── models.py          # Book and Loan models
│   ├── serializers.py     # Book and Loan serializers
│   ├── views.py           # Book and Loan views
│   ├── filters.py         # Custom filters
│   ├── permissions.py     # Custom permissions
│   ├── tests.py           # Model tests
│   └── test_api.py        # API tests
├── library_project/       # Project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── factories.py           # Test factories
├── conftest.py            # Pytest configuration
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── Procfile               # Heroku configuration
├── runtime.txt            # Python version for Heroku
├── pytest.ini             # Pytest settings
├── .coveragerc            # Coverage configuration
└── README.md              # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Django REST Framework documentation
- Django documentation
- PostgreSQL documentation
- Docker documentation

## 📞 Support

For support, email support@library.local or create an issue in the repository.

## 🔄 Future Enhancements

- Email notifications for overdue books
- Book reservation system
- Fine calculation for overdue books
- Book reviews and ratings
- Reading lists and recommendations
- Export reports (PDF, Excel)
- Mobile app integration
- Multi-library support
- Book cover upload
- Advanced analytics dashboard
