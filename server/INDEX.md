# 📚 Library Management System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-55%2B-brightgreen.svg)](#testing)
[![Coverage](https://img.shields.io/badge/Coverage-85%25-brightgreen.svg)](#testing)

A full-featured Django REST Framework application for managing library operations with comprehensive functionality including user authentication, book management, loan tracking, and administrative tools.

---

## 🌟 Key Features

### 👥 User Management
- User registration with email validation
- JWT-based authentication (access & refresh tokens)
- Role-based access control (User/Admin)
- Profile management and password reset
- Admin panel for user management

### 📚 Book Management
- Anonymous browsing of books
- Advanced search and filtering
- Category-based organization
- ISBN-based unique identification
- Availability tracking
- Admin CRUD operations

### 📖 Loan System
- Borrow and return books
- Automatic due date calculation (14 days)
- Overdue tracking and notifications
- Prevent duplicate active loans
- Comprehensive loan history
- Admin oversight of all loans

### 🔒 Security
- JWT authentication with configurable lifetime
- Password validation and hashing
- CSRF, XSS, and SQL injection protection
- Secure headers and cookie settings
- Role-based permissions

### 📊 API Features
- RESTful design principles
- Comprehensive filtering and pagination
- Search across multiple fields
- Swagger/ReDoc documentation
- Standardized error responses

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone and start
git clone <repository-url>
cd library_mgmt
docker-compose up

# Initialize database (in another terminal)
docker-compose exec web bash init_db.sh

# Access the application
# API: http://localhost:8000
# Admin: http://localhost:8000/admin (admin/admin123)
# Docs: http://localhost:8000/swagger
```

### Option 2: Local Development

```bash
# Clone repository
git clone <repository-url>
cd library_mgmt

# Run setup script
./setup.sh

# Follow the interactive prompts
# Then access at http://localhost:8000
```

### Option 3: Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Setup database
python manage.py migrate
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | Complete project documentation |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute quick start guide |
| [API_EXAMPLES.md](API_EXAMPLES.md) | API usage examples with curl/Python/JavaScript |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Comprehensive project overview |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **Admin Panel**: http://localhost:8000/admin/

---

## 🎯 API Endpoints

### Authentication
```
POST   /api/auth/register/              # Register new user
POST   /api/auth/login/                 # Login with JWT
POST   /api/auth/token/refresh/         # Refresh token
GET    /api/auth/profile/               # Get user profile
PATCH  /api/auth/profile/               # Update profile
POST   /api/auth/change-password/       # Change password
```

### Books
```
GET    /api/books/                      # List all books (public)
POST   /api/books/                      # Create book (admin)
GET    /api/books/{id}/                 # Get book details
PUT    /api/books/{id}/                 # Update book (admin)
DELETE /api/books/{id}/                 # Delete book (admin)
GET    /api/books/search/?q=query       # Search books
```

### Loans
```
GET    /api/loans/                      # Get user's loans
POST   /api/loans/borrow/               # Borrow a book
POST   /api/loans/return/               # Return a book
GET    /api/admin/loans/                # All loans (admin)
GET    /api/admin/loans/overdue/        # Overdue loans (admin)
```

### Admin
```
GET    /api/auth/users/                 # List all users (admin)
GET    /api/auth/users/{id}/            # Get user details (admin)
PATCH  /api/auth/users/{id}/            # Update user (admin)
DELETE /api/auth/users/{id}/            # Deactivate user (admin)
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html

# Run specific tests
pytest accounts/test_api.py
pytest books/tests.py
```

**Test Statistics:**
- Total Tests: 55+
- Test Coverage: ~85%
- All endpoints covered
- Success and failure cases tested

---

## 🛠️ Technology Stack

### Backend Framework
- **Django 4.2.7** - High-level Python web framework
- **Django REST Framework 3.14.0** - Powerful toolkit for building APIs
- **Simple JWT 5.3.0** - JSON Web Token authentication

### Database
- **PostgreSQL 15** - Production database
- **SQLite** - Development database

### Tools & Libraries
- **django-filter** - Advanced filtering
- **drf-yasg** - Swagger/OpenAPI documentation
- **WhiteNoise** - Static file serving
- **Gunicorn** - WSGI HTTP server
- **pytest** - Testing framework
- **factory-boy** - Test data generation

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Heroku** - Deployment platform (configured)

---

## 📁 Project Structure

```
library_mgmt/
├── 📱 accounts/              User authentication & management
│   ├── models.py            Custom User model
│   ├── serializers.py       User serializers
│   ├── views.py             Authentication views
│   ├── permissions.py       Custom permissions
│   ├── admin.py             User admin configuration
│   └── tests/               Comprehensive tests
│
├── 📚 books/                Book & loan management
│   ├── models.py            Book & Loan models
│   ├── serializers.py       Book & Loan serializers
│   ├── views.py             Book & Loan views
│   ├── filters.py           Custom filters
│   ├── permissions.py       Access control
│   ├── admin.py             Admin configuration
│   └── tests/               API & model tests
│
├── ⚙️ library_project/      Project configuration
│   ├── settings.py          Django settings
│   ├── urls.py              URL routing
│   ├── wsgi.py              WSGI configuration
│   └── asgi.py              ASGI configuration
│
├── 🐳 Docker files
│   ├── Dockerfile           Container definition
│   ├── docker-compose.yml   Service orchestration
│   └── init_db.sh          Database initialization
│
├── 📋 Documentation
│   ├── README.md            Main documentation
│   ├── QUICKSTART.md        Quick start guide
│   ├── API_EXAMPLES.md      API usage examples
│   ├── PROJECT_SUMMARY.md   Project overview
│   └── CONTRIBUTING.md      Contribution guide
│
├── 🧪 Testing
│   ├── conftest.py          Pytest configuration
│   ├── factories.py         Test data factories
│   ├── pytest.ini           Test settings
│   └── .coveragerc          Coverage configuration
│
├── 🚀 Deployment
│   ├── Procfile             Heroku process file
│   ├── runtime.txt          Python version
│   ├── app.json             Heroku app config
│   └── requirements.txt     Python dependencies
│
└── 🔧 Scripts
    ├── setup.sh             Interactive setup
    ├── verify_setup.sh      Setup verification
    └── create_sample_data.py Sample data generator
```

---

## 🎨 Sample Usage

### Register and Login

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "SecurePass123!"
  }'
```

### Browse and Borrow Books

```bash
# List books (no auth required)
curl http://localhost:8000/api/books/

# Search books
curl http://localhost:8000/api/books/search/?q=gatsby \
  -H "Authorization: Bearer YOUR_TOKEN"

# Borrow a book
curl -X POST http://localhost:8000/api/loans/borrow/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"book_id": 1}'
```

See [API_EXAMPLES.md](API_EXAMPLES.md) for more examples in curl, Python, and JavaScript.

---

## 🔧 Configuration

### Environment Variables

```bash
# Security
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60      # minutes
JWT_REFRESH_TOKEN_LIFETIME=1440   # minutes
```

---

## 📊 Database Schema

### Models Overview

**User**
- Authentication & profile information
- Role-based access (user/admin)
- Contact details and address

**Book**
- Complete bibliographic information
- ISBN-based unique identification
- Availability tracking
- Category organization

**Loan**
- Borrowing transactions
- Due date management
- Status tracking (active/returned/overdue)
- Return history

---

## 🎯 User Permissions

| Action | Anonymous | User | Admin |
|--------|-----------|------|-------|
| Browse Books | ✅ | ✅ | ✅ |
| Search Books | ❌ | ✅ | ✅ |
| Borrow Books | ❌ | ✅ | ✅ |
| Return Books | ❌ | ✅ | ✅ |
| Add/Edit Books | ❌ | ❌ | ✅ |
| Delete Books | ❌ | ❌ | ✅ |
| View All Loans | ❌ | ❌ | ✅ |
| Manage Users | ❌ | ❌ | ✅ |

---

## 🚢 Deployment

### Heroku Deployment

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Docker Deployment

```bash
# Build image
docker build -t library-management .

# Run container
docker run -p 8000:8000 \
  -e SECRET_KEY="your-secret-key" \
  -e DB_HOST="your-db-host" \
  library-management
```

See [README.md](README.md) for detailed deployment instructions.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Commit your changes (`git commit -m 'feat: add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

- 📖 **Documentation**: Check our comprehensive docs
- 💬 **Issues**: Open an issue on GitHub
- 📧 **Email**: support@library.local
- 🌐 **API Docs**: http://localhost:8000/swagger/

---

## 🏆 Project Status

✅ **Complete** - All requirements implemented and tested

### Features Implemented
- ✅ User authentication & authorization
- ✅ Book management system
- ✅ Loan tracking system
- ✅ Admin panel
- ✅ API documentation
- ✅ Comprehensive testing (55+ tests)
- ✅ Docker support
- ✅ Deployment configuration
- ✅ Security best practices
- ✅ Filtering & pagination

---

## 📈 Statistics

- **Total Endpoints**: 20+
- **Test Coverage**: ~85%
- **Lines of Code**: 3000+
- **Documentation Pages**: 7
- **Sample Books**: 15
- **Test Cases**: 55+

---

## 🙏 Acknowledgments

- Django and Django REST Framework communities
- PostgreSQL team
- Docker team
- All contributors

---

## 📞 Contact

For questions or support, please:
- Open an issue on GitHub
- Email: support@library.local
- Check the documentation

---

**Made with ❤️ using Django and Django REST Framework**

---

## Quick Links

- [📖 Full Documentation](README.md)
- [⚡ Quick Start](QUICKSTART.md)
- [💻 API Examples](API_EXAMPLES.md)
- [📊 Project Summary](PROJECT_SUMMARY.md)
- [🤝 Contributing](CONTRIBUTING.md)
- [🌐 Swagger Docs](http://localhost:8000/swagger/)

---

**Happy Coding! 🚀**
