# Library Management System - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Option 1: Using Docker (Recommended)

1. **Prerequisites**
   - Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

2. **Clone and Start**
   ```bash
   git clone <repository-url>
   cd library_management
   docker-compose up -d
   ```

3. **Initialize Database**
   ```bash
   docker-compose exec backend python manage.py migrate
   docker-compose exec backend python manage.py createsuperuser
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin
   - API Docs: http://localhost:8000/swagger

### Option 2: Manual Setup

#### Backend Setup
```bash
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

#### Frontend Setup (New Terminal)
```bash
cd client
npm install
cp .env.local.example .env.local
npm run dev
```

## 📖 First Steps

### 1. Create Admin Account
```bash
docker-compose exec backend python manage.py createsuperuser
```
Follow the prompts to set username, email, and password.

### 2. Add Sample Books (Optional)
```bash
docker-compose exec backend python create_sample_data.py
```

### 3. Login
- Go to http://localhost:3000
- Click "Sign Up" to create a user account, or
- Click "Login" with your admin credentials

### 4. Browse Books
- Navigate to "Browse Books"
- Search, filter, and view book details
- Borrow books (requires login)

### 5. Admin Panel
- Login with admin credentials
- Go to "Admin Panel"
- Add, edit, or delete books
- View statistics and manage loans

## 🎯 Key Features to Try

1. **Search & Filter**: Use the search bar on the books page
2. **Borrow a Book**: Click "Borrow" on any available book
3. **My Loans**: View your borrowed books and return them
4. **Profile**: Update your personal information
5. **Admin Dashboard**: Access admin features (admin users only)

## 🔧 Common Commands

### Docker
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart backend
docker-compose restart frontend

# Execute commands
docker-compose exec backend python manage.py <command>
```

### Development
```bash
# Backend
python manage.py runserver
python manage.py test
pytest

# Frontend
npm run dev
npm run build
npm run lint
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Database Connection Error
```bash
# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db
```

### Frontend Not Loading
```bash
# Rebuild frontend
docker-compose up -d --build frontend

# Check logs
docker-compose logs frontend
```

### Backend Errors
```bash
# Check backend logs
docker-compose logs backend

# Run migrations
docker-compose exec backend python manage.py migrate
```

## 📚 API Testing

### Using curl
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123","password2":"testpass123","first_name":"Test","last_name":"User"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Get books
curl http://localhost:8000/api/books/
```

### Using Swagger UI
Visit http://localhost:8000/swagger for interactive API documentation.

## 🎨 Customization

### Change Theme Colors
Edit `client/tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom colors
      }
    }
  }
}
```

### Update Logo
Replace the logo in `client/components/Navbar.tsx`

### Add More Book Categories
Categories are dynamic based on books in the database.

## 📞 Need Help?

- Check the [full README](README.md)
- Review [API Examples](server/API_EXAMPLES.md)
- Visit API documentation at http://localhost:8000/swagger
- Create an issue on GitHub

## ✅ Checklist

- [ ] Docker is installed and running
- [ ] All services are running (`docker-compose ps`)
- [ ] Database is initialized (migrations run)
- [ ] Admin user is created
- [ ] Can access frontend (http://localhost:3000)
- [ ] Can access backend API (http://localhost:8000)
- [ ] Can login successfully

## 🎉 You're All Set!

Start exploring the library management system. Happy reading! 📚
