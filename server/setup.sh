#!/bin/bash

# Library Management System - Setup Script
# This script helps you set up the project quickly

set -e

echo "=========================================="
echo "Library Management System - Setup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓${NC} Python $python_version found"
echo ""

# Ask setup method
echo "Choose setup method:"
echo "1) Docker (Recommended - includes PostgreSQL)"
echo "2) Local development with virtual environment"
read -p "Enter choice (1 or 2): " setup_choice
echo ""

if [ "$setup_choice" == "1" ]; then
    # Docker setup
    echo "=========================================="
    echo "Docker Setup"
    echo "=========================================="
    echo ""
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo -e "${YELLOW}Warning:${NC} Docker is not installed."
        echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    
    echo -e "${GREEN}✓${NC} Docker found"
    
    # Check if Docker Compose is available
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null 2>&1; then
        echo -e "${YELLOW}Warning:${NC} Docker Compose is not available."
        exit 1
    fi
    
    echo -e "${GREEN}✓${NC} Docker Compose found"
    echo ""
    
    # Build and start containers
    echo "Building Docker containers..."
    docker-compose build
    echo ""
    
    echo "Starting containers..."
    docker-compose up -d
    echo ""
    
    # Wait for database to be ready
    echo "Waiting for database to be ready..."
    sleep 10
    
    # Initialize database
    echo "Initializing database..."
    docker-compose exec -T web python manage.py migrate
    echo ""
    
    # Create superuser
    echo "Creating superuser..."
    docker-compose exec -T web python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='admin')
    print('Superuser created!')
else:
    print('Superuser already exists.')
END
    echo ""
    
    echo -e "${GREEN}✓${NC} Setup completed successfully!"
    echo ""
    echo "=========================================="
    echo "Access Information:"
    echo "=========================================="
    echo "API: http://localhost:8000"
    echo "Admin Panel: http://localhost:8000/admin"
    echo "API Docs: http://localhost:8000/swagger"
    echo ""
    echo "Default Admin Credentials:"
    echo "Username: admin"
    echo "Password: admin123"
    echo ""
    echo "To stop: docker-compose down"
    echo "To view logs: docker-compose logs -f"
    
elif [ "$setup_choice" == "2" ]; then
    # Local setup
    echo "=========================================="
    echo "Local Development Setup"
    echo "=========================================="
    echo ""
    
    # Create virtual environment
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
    echo ""
    
    # Activate virtual environment
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo ""
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo -e "${GREEN}✓${NC} Dependencies installed"
    echo ""
    
    # Create .env file
    if [ ! -f .env ]; then
        echo "Creating .env file..."
        cp .env.example .env
        
        # Generate secret key
        secret_key=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
        
        # Update .env with SQLite for quick start
        cat > .env << EOF
SECRET_KEY=$secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (SQLite for quick start)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# JWT Configuration
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
EOF
        echo -e "${GREEN}✓${NC} .env file created with SQLite configuration"
    else
        echo -e "${YELLOW}Note:${NC} .env file already exists, skipping..."
    fi
    echo ""
    
    # Run migrations
    echo "Running database migrations..."
    python manage.py migrate
    echo -e "${GREEN}✓${NC} Migrations completed"
    echo ""
    
    # Create superuser
    echo "Creating superuser..."
    echo "Username: admin"
    echo "Email: admin@example.com"
    echo "Password: admin123"
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='admin')
    print('Superuser created!')
else:
    print('Superuser already exists.')
END
    echo ""
    
    # Collect static files
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
    echo ""
    
    echo -e "${GREEN}✓${NC} Setup completed successfully!"
    echo ""
    echo "=========================================="
    echo "Next Steps:"
    echo "=========================================="
    echo "1. Activate virtual environment:"
    echo "   source venv/bin/activate"
    echo ""
    echo "2. Start the development server:"
    echo "   python manage.py runserver"
    echo ""
    echo "3. Access the application:"
    echo "   API: http://localhost:8000"
    echo "   Admin: http://localhost:8000/admin"
    echo "   Docs: http://localhost:8000/swagger"
    echo ""
    echo "Default Admin Credentials:"
    echo "Username: admin"
    echo "Password: admin123"
    echo ""
    echo "4. Run tests:"
    echo "   pytest"
    
else
    echo "Invalid choice. Please run the script again and choose 1 or 2."
    exit 1
fi

echo ""
echo "=========================================="
echo "For more information, see:"
echo "- README.md for detailed documentation"
echo "- QUICKSTART.md for quick start guide"
echo "- API_EXAMPLES.md for API usage examples"
echo "=========================================="
