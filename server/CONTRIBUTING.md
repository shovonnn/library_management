# Contributing to Library Management System

Thank you for considering contributing to the Library Management System! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL 15+ (or SQLite for development)
- Git
- Docker (optional)

### Setup Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/library_mgmt.git
   cd library_mgmt
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## Development Workflow

### Branch Naming Convention
- `feature/feature-name` - New features
- `bugfix/bug-description` - Bug fixes
- `hotfix/critical-fix` - Critical production fixes
- `docs/documentation-update` - Documentation updates
- `refactor/code-improvement` - Code refactoring

### Example Workflow

1. **Create a Branch**
   ```bash
   git checkout -b feature/add-book-reviews
   ```

2. **Make Changes**
   - Write your code
   - Add tests
   - Update documentation

3. **Test Your Changes**
   ```bash
   pytest
   pytest --cov=. --cov-report=html
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add book review functionality"
   ```

5. **Push to Fork**
   ```bash
   git push origin feature/add-book-reviews
   ```

6. **Create Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Fill in the PR template

## Coding Standards

### Python Style Guide
We follow PEP 8 with some modifications:
- Line length: 100 characters (not 79)
- Use 4 spaces for indentation
- Use descriptive variable names
- Add docstrings to all functions and classes

### Django Best Practices
- Use class-based views for complex logic
- Keep views thin, models fat
- Use serializers for data validation
- Follow DRF conventions

### Example Code Style

```python
class BookListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating books.
    
    GET: List all books with pagination and filtering
    POST: Create a new book (admin only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter
    
    def get_serializer_class(self):
        """Return appropriate serializer based on request method."""
        if self.request.method == 'GET':
            return BookListSerializer
        return BookSerializer
```

### Code Organization
- Keep related functionality together
- Use meaningful file and function names
- Avoid deeply nested code
- Extract complex logic into separate functions

## Testing Guidelines

### Test Coverage
- Aim for 80%+ code coverage
- Write tests for all new features
- Update tests when modifying existing features
- Test both success and failure cases

### Test Structure

```python
@pytest.mark.django_db
class TestBookAPI:
    """Test cases for Book API endpoints."""
    
    def setup_method(self):
        """Setup test client and data."""
        self.client = APIClient()
        self.user = UserFactory()
        self.admin = AdminUserFactory()
    
    def test_list_books(self):
        """Test listing books endpoint."""
        BookFactory.create_batch(5)
        response = self.client.get('/api/books/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 5
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest accounts/test_api.py

# Specific test
pytest accounts/test_api.py::TestAuthenticationAPI::test_user_registration

# With coverage
pytest --cov=. --cov-report=html

# Verbose output
pytest -v
```

## Commit Messages

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

**Good Commit Messages:**
```
feat(books): add book review functionality

Add API endpoints for users to review books:
- POST /api/books/{id}/reviews/
- GET /api/books/{id}/reviews/
- Include rating and comment fields

Closes #123
```

```
fix(loans): prevent borrowing unavailable books

Add validation to check book availability before
creating a loan. Update tests to cover edge cases.

Fixes #456
```

**Bad Commit Messages:**
```
update stuff
fixed bug
WIP
asdfasdf
```

## Pull Request Process

### Before Submitting

1. **Ensure All Tests Pass**
   ```bash
   pytest
   ```

2. **Check Code Coverage**
   ```bash
   pytest --cov=. --cov-report=term-missing
   ```

3. **Update Documentation**
   - Update README if needed
   - Add API examples if adding endpoints
   - Update docstrings

4. **Run Linting** (if configured)
   ```bash
   flake8 .
   black --check .
   ```

### PR Template

When creating a PR, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] All tests pass
- [ ] New tests added
- [ ] Coverage maintained/improved

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated

## Related Issues
Closes #123
```

### Review Process

1. A maintainer will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged

### After Your PR is Merged

1. Delete your feature branch
2. Update your local repository
   ```bash
   git checkout main
   git pull upstream main
   ```

## API Design Guidelines

### RESTful Principles
- Use appropriate HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Return appropriate status codes
- Use plural nouns for endpoints
- Keep URLs consistent

### Status Codes
- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

### Response Format

```json
{
  "data": { ... },
  "message": "Success message",
  "errors": null
}
```

## Database Migrations

### Creating Migrations

```bash
# After model changes
python manage.py makemigrations

# Review the migration
cat apps/*/migrations/0001_initial.py

# Apply migrations
python manage.py migrate
```

### Migration Best Practices
- Review auto-generated migrations
- Add data migrations when needed
- Test migrations on development database
- Never edit applied migrations

## Documentation

### Code Documentation
- Add docstrings to all classes and functions
- Use type hints where appropriate
- Keep comments up-to-date

### API Documentation
- Update Swagger annotations
- Add examples for complex endpoints
- Document all query parameters

## Security

### Reporting Security Issues
- Do NOT open public issues for security vulnerabilities
- Email security concerns to: security@example.com
- Include detailed description and reproduction steps

### Security Best Practices
- Never commit secrets or credentials
- Use environment variables for sensitive data
- Validate all user input
- Use parameterized queries
- Keep dependencies updated

## Questions?

- Open an issue for general questions
- Join our community chat (if available)
- Check existing issues and PRs
- Review documentation

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
