# Library Management System

A full-stack library management application with a Django REST API backend and Next.js frontend. Users can browse and borrow books, while administrators can manage the book inventory and monitor loans.

## 🚀 Features

### For Users
- 📚 Browse and search books by title, author, or category
- 🔍 Advanced filtering and pagination
- 📖 View detailed book information
- 📋 Borrow and return books
- 📅 Track loan history and due dates
- 👤 Manage personal profile
- 🔐 Secure authentication with JWT

### For Administrators
- 📊 Dashboard with library statistics
- ➕ Add, edit, and delete books
- 👥 Monitor all loans and users
- 📈 View borrowing trends

## 🛠️ Tech Stack

### Backend
- Django 4.2
- Django REST Framework
- MySQL/PostgreSQL
- JWT Authentication
- Docker

### Frontend
- Next.js 14 (TypeScript)
- Tailwind CSS
- Zustand (State Management)
- Axios
- React Hook Form

## 📋 Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

## 🚀 Quick Start with Docker

### 1. Clone the Repository

```bash
git clone <repository-url>
cd library_management
```

### 2. Start All Services

```bash
docker-compose up -d
```

This will start:
- **MySQL Database** on port 3306
- **Django Backend** on port 8000
- **Next.js Frontend** on port 3000

### 3. Initialize Database (First Time Only)

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# (Optional) Load sample data
docker-compose exec backend python create_sample_data.py
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **Admin Panel**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/swagger

## 🔧 Local Development Setup

### Backend Setup

```bash
cd server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Frontend Setup

```bash
cd client

# Install dependencies
npm install

# Copy environment file
cp .env.local.example .env.local

# Run development server
npm run dev
```

## 📁 Project Structure

```
library_management/
├── server/                 # Django backend
│   ├── accounts/          # User authentication
│   ├── books/             # Books and loans
│   ├── library_project/   # Project settings
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── client/                # Next.js frontend
│   ├── app/              # Next.js pages
│   ├── components/       # React components
│   ├── lib/              # Utilities & services
│   ├── styles/           # Global styles
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml    # Docker orchestration
```

## 🔑 Default Credentials

After creating a superuser, you can login with those credentials. For testing with sample data:

- **Admin**: username: `admin`, password: (set during superuser creation)
- **Regular User**: username: `testuser`, password: `testpass123`

## 📚 API Documentation

The API is fully documented using Swagger/OpenAPI:

- **Swagger UI**: http://localhost:8000/swagger
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login
- `GET /api/auth/profile/` - Get user profile
- `POST /api/auth/change-password/` - Change password

#### Books
- `GET /api/books/` - List all books
- `GET /api/books/{id}/` - Get book details
- `POST /api/books/` - Add book (admin only)
- `PATCH /api/books/{id}/` - Update book (admin only)
- `DELETE /api/books/{id}/` - Delete book (admin only)

#### Loans
- `POST /api/loans/` - Borrow a book
- `GET /api/loans/my-loans/` - Get user's loans
- `POST /api/loans/{id}/return/` - Return a book

## 🧪 Testing

### Backend Tests

```bash
cd server
pytest
pytest --cov  # With coverage
```

### Frontend Tests

```bash
cd client
npm test
```

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild services
docker-compose up -d --build

# Execute commands in containers
docker-compose exec backend python manage.py migrate
docker-compose exec frontend npm run build
```

## 🔒 Security Features

- JWT-based authentication
- Password hashing with Django's built-in system
- CORS configuration
- SQL injection prevention
- XSS protection
- CSRF protection

## 📊 Database Schema

### User Model
- Extended Django User with custom fields
- Roles: admin, user
- Additional fields: phone_number, address

### Book Model
- Title, author, ISBN
- Publisher, publication date
- Category, language
- Available and total copies
- Cover image URL

### Loan Model
- User and book relationships
- Borrow and due dates
- Return date
- Status: borrowed, returned, overdue
- Fine calculation

## 🌐 Environment Variables

### Backend (.env)
```
DEBUG=False
SECRET_KEY=your-secret-key
DB_ENGINE=django.db.backends.mysql
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=library_password
DB_HOST=db
DB_PORT=3306
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## 📱 Responsive Design

The frontend is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## 🚀 Deployment

### Production Considerations

1. **Security**:
   - Change all default passwords
   - Set strong SECRET_KEY
   - Use HTTPS
   - Configure ALLOWED_HOSTS

2. **Database**:
   - Use managed database service
   - Regular backups
   - Connection pooling

3. **Frontend**:
   - Build optimization
   - CDN for static assets
   - Environment-specific API URLs

4. **Backend**:
   - Use production WSGI server (Gunicorn)
   - Configure static files serving
   - Set DEBUG=False

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Development Team

## 🙏 Acknowledgments

- Django REST Framework documentation
- Next.js documentation
- Tailwind CSS
- All open-source contributors

## 📞 Support

For support, email support@libraryhub.com or create an issue on GitHub.

## 🎯 Roadmap

- [ ] Email notifications for due dates
- [ ] Book reservations
- [ ] Reviews and ratings
- [ ] Reading recommendations
- [ ] Mobile app (React Native)
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Integration with library systems

## ⚡ Performance

- Backend: Django ORM optimization with select_related
- Frontend: Next.js SSR and code splitting
- Database: Indexed fields for faster queries
- Caching: Redis integration (optional)

## 🔍 Monitoring

Recommended tools:
- Sentry for error tracking
- Google Analytics for usage
- Django Debug Toolbar (development)
- Docker stats for resource monitoring

---

Made with ❤️ by the LibraryHub Team
