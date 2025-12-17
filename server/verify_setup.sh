#!/bin/bash

# Library Management System - Verification Script
# This script verifies that all components are properly set up

echo "=========================================="
echo "Library Management System - Verification"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
PASSED=0
FAILED=0
WARNING=0

# Helper function for checks
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $1"
        ((FAILED++))
    fi
}

check_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNING++))
}

# Check Python
echo "Checking Python..."
python3 --version > /dev/null 2>&1
check "Python 3 is installed"

# Check project structure
echo ""
echo "Checking project structure..."
[ -f "manage.py" ] && check "manage.py exists" || check "manage.py exists"
[ -f "requirements.txt" ] && check "requirements.txt exists" || check "requirements.txt exists"
[ -d "library_project" ] && check "library_project directory exists" || check "library_project directory exists"
[ -d "accounts" ] && check "accounts app exists" || check "accounts app exists"
[ -d "books" ] && check "books app exists" || check "books app exists"

# Check configuration files
echo ""
echo "Checking configuration files..."
[ -f ".env.example" ] && check ".env.example exists" || check ".env.example exists"
[ -f "Dockerfile" ] && check "Dockerfile exists" || check "Dockerfile exists"
[ -f "docker-compose.yml" ] && check "docker-compose.yml exists" || check "docker-compose.yml exists"
[ -f "Procfile" ] && check "Procfile exists" || check "Procfile exists"
[ -f "pytest.ini" ] && check "pytest.ini exists" || check "pytest.ini exists"

# Check documentation
echo ""
echo "Checking documentation..."
[ -f "README.md" ] && check "README.md exists" || check "README.md exists"
[ -f "QUICKSTART.md" ] && check "QUICKSTART.md exists" || check "QUICKSTART.md exists"
[ -f "API_EXAMPLES.md" ] && check "API_EXAMPLES.md exists" || check "API_EXAMPLES.md exists"
[ -f "PROJECT_SUMMARY.md" ] && check "PROJECT_SUMMARY.md exists" || check "PROJECT_SUMMARY.md exists"
[ -f "CONTRIBUTING.md" ] && check "CONTRIBUTING.md exists" || check "CONTRIBUTING.md exists"

# Check scripts
echo ""
echo "Checking scripts..."
[ -f "setup.sh" ] && [ -x "setup.sh" ] && check "setup.sh is executable" || check "setup.sh is executable"
[ -f "init_db.sh" ] && [ -x "init_db.sh" ] && check "init_db.sh is executable" || check "init_db.sh is executable"
[ -f "create_sample_data.py" ] && check "create_sample_data.py exists" || check "create_sample_data.py exists"

# Check if virtual environment exists
echo ""
echo "Checking Python environment..."
if [ -d "venv" ]; then
    check "Virtual environment exists"
    
    # Check if dependencies are installed
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        python -c "import django" 2>/dev/null && check "Django is installed" || check_warning "Django is not installed"
        python -c "import rest_framework" 2>/dev/null && check "Django REST Framework is installed" || check_warning "DRF is not installed"
        deactivate
    fi
else
    check_warning "Virtual environment not found (run setup.sh to create)"
fi

# Check Docker (optional)
echo ""
echo "Checking Docker (optional)..."
if command -v docker &> /dev/null; then
    check "Docker is installed"
    
    if command -v docker-compose &> /dev/null || docker compose version &> /dev/null 2>&1; then
        check "Docker Compose is available"
    else
        check_warning "Docker Compose is not available"
    fi
else
    check_warning "Docker is not installed (optional for development)"
fi

# Check PostgreSQL (optional)
echo ""
echo "Checking PostgreSQL (optional)..."
if command -v psql &> /dev/null; then
    check "PostgreSQL client is installed"
else
    check_warning "PostgreSQL not found (you can use SQLite for development)"
fi

# Check model files
echo ""
echo "Checking model definitions..."
[ -f "accounts/models.py" ] && grep -q "class User" accounts/models.py && check "User model defined" || check "User model defined"
[ -f "books/models.py" ] && grep -q "class Book" books/models.py && check "Book model defined" || check "Book model defined"
[ -f "books/models.py" ] && grep -q "class Loan" books/models.py && check "Loan model defined" || check "Loan model defined"

# Check view files
echo ""
echo "Checking views..."
[ -f "accounts/views.py" ] && check "accounts/views.py exists" || check "accounts/views.py exists"
[ -f "books/views.py" ] && check "books/views.py exists" || check "books/views.py exists"

# Check serializers
echo ""
echo "Checking serializers..."
[ -f "accounts/serializers.py" ] && check "accounts/serializers.py exists" || check "accounts/serializers.py exists"
[ -f "books/serializers.py" ] && check "books/serializers.py exists" || check "books/serializers.py exists"

# Check URL configuration
echo ""
echo "Checking URL configuration..."
[ -f "library_project/urls.py" ] && grep -q "swagger" library_project/urls.py && check "Swagger URLs configured" || check "Swagger URLs configured"
[ -f "accounts/urls.py" ] && check "accounts URLs exist" || check "accounts URLs exist"
[ -f "books/urls.py" ] && check "books URLs exist" || check "books URLs exist"

# Check tests
echo ""
echo "Checking tests..."
[ -f "accounts/tests.py" ] && check "accounts/tests.py exists" || check "accounts/tests.py exists"
[ -f "accounts/test_api.py" ] && check "accounts/test_api.py exists" || check "accounts/test_api.py exists"
[ -f "books/tests.py" ] && check "books/tests.py exists" || check "books/tests.py exists"
[ -f "books/test_api.py" ] && check "books/test_api.py exists" || check "books/test_api.py exists"
[ -f "factories.py" ] && check "factories.py exists" || check "factories.py exists"
[ -f "conftest.py" ] && check "conftest.py exists" || check "conftest.py exists"

# Check admin configuration
echo ""
echo "Checking admin configuration..."
[ -f "accounts/admin.py" ] && grep -q "@admin.register" accounts/admin.py && check "User admin registered" || check "User admin registered"
[ -f "books/admin.py" ] && grep -q "@admin.register" books/admin.py && check "Book admin registered" || check "Book admin registered"

# Check permissions
echo ""
echo "Checking custom permissions..."
[ -f "accounts/permissions.py" ] && check "accounts permissions exist" || check "accounts permissions exist"
[ -f "books/permissions.py" ] && check "books permissions exist" || check "books permissions exist"

# Check filters
echo ""
echo "Checking filters..."
[ -f "books/filters.py" ] && check "books filters exist" || check "books filters exist"

# Check settings
echo ""
echo "Checking settings configuration..."
grep -q "rest_framework" library_project/settings.py && check "REST Framework configured" || check "REST Framework configured"
grep -q "SIMPLE_JWT" library_project/settings.py && check "JWT configured" || check "JWT configured"
grep -q "drf_yasg" library_project/settings.py && check "Swagger configured" || check "Swagger configured"

# Summary
echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo -e "${GREEN}Passed:${NC} $PASSED"
echo -e "${RED}Failed:${NC} $FAILED"
echo -e "${YELLOW}Warnings:${NC} $WARNING"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All critical checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Run: ./setup.sh (if not already done)"
    echo "2. Run: python manage.py runserver"
    echo "3. Visit: http://localhost:8000/swagger/"
    echo ""
    echo "Or use Docker:"
    echo "1. Run: docker-compose up"
    echo "2. Run: docker-compose exec web bash init_db.sh"
    echo "3. Visit: http://localhost:8000/swagger/"
else
    echo -e "${RED}✗ Some checks failed. Please review the output above.${NC}"
    exit 1
fi

echo "=========================================="
