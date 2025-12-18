import pytest
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
from factories import UserFactory, AdminUserFactory, BookFactory, LoanFactory
from books.models import Book, Loan


@pytest.mark.django_db
class TestBookAPI:
    """Test cases for Book API endpoints."""
    
    def setup_method(self):
        """Setup test client."""
        self.client = APIClient()
        # Clean up any existing data
        Book.objects.all().delete()
        Loan.objects.all().delete()
    
    def test_anonymous_user_can_view_books(self):
        """Test anonymous users can view books."""
        BookFactory.create_batch(5)
        response = self.client.get('/api/books/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 5
    
    def test_anonymous_user_cannot_create_book(self):
        """Test anonymous users cannot create books."""
        data = {
            'title': 'New Book',
            'author': 'Author Name',
            'isbn': '9781234567890',
            'page_count': 300,
            'category': 'Fiction',
            'total_copies': 5,
            'available_copies': 5
        }
        response = self.client.post('/api/books/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_regular_user_cannot_create_book(self):
        """Test regular users cannot create books."""
        user = UserFactory()
        self.client.force_authenticate(user=user)
        
        data = {
            'title': 'New Book',
            'author': 'Author Name',
            'isbn': '9781234567890',
            'page_count': 300,
            'category': 'Fiction',
            'total_copies': 5,
            'available_copies': 5
        }
        response = self.client.post('/api/books/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_admin_can_create_book(self):
        """Test admin can create books."""
        admin = AdminUserFactory()
        self.client.force_authenticate(user=admin)
        
        data = {
            'title': 'New Book',
            'author': 'Author Name',
            'isbn': '9781234567890',
            'page_count': 300,
            'category': 'Fiction',
            'total_copies': 5,
            'available_copies': 5
        }
        response = self.client.post('/api/books/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.filter(isbn='9781234567890').exists()
    
    def test_admin_can_update_book(self):
        """Test admin can update books."""
        admin = AdminUserFactory()
        book = BookFactory()
        self.client.force_authenticate(user=admin)
        
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/books/{book.id}/', data)
        
        assert response.status_code == status.HTTP_200_OK
        book.refresh_from_db()
        assert book.title == 'Updated Title'
    
    def test_admin_can_delete_book(self):
        """Test admin can delete books."""
        admin = AdminUserFactory()
        book = BookFactory()
        self.client.force_authenticate(user=admin)
        
        response = self.client.delete(f'/api/books/{book.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Book.objects.filter(id=book.id).exists()
    
    def test_search_books(self):
        """Test book search functionality."""
        user = UserFactory()
        self.client.force_authenticate(user=user)
        
        BookFactory(title='Python Programming')
        BookFactory(title='Java Basics')
        BookFactory(author='Python Master')
        
        response = self.client.get('/api/books/search/?q=Python')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_filter_books_by_category(self):
        """Test filtering books by category."""
        BookFactory.create_batch(3, category='Fiction')
        BookFactory.create_batch(2, category='Science')
        
        response = self.client.get('/api/books/?category=Fiction')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
    
    def test_filter_available_books(self):
        """Test filtering available books."""
        BookFactory.create_batch(3, available_copies=5)
        BookFactory.create_batch(2, available_copies=0)
        
        response = self.client.get('/api/books/?available=true')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3


@pytest.mark.django_db
class TestLoanAPI:
    """Test cases for Loan API endpoints."""
    
    def setup_method(self):
        """Setup test client."""
        self.client = APIClient()
        # Clean up any existing data
        Loan.objects.all().delete()
        Book.objects.all().delete()
    
    def test_borrow_book(self):
        """Test borrowing a book."""
        user = UserFactory()
        book = BookFactory(available_copies=5)
        self.client.force_authenticate(user=user)
        
        data = {'book_id': book.id}
        response = self.client.post('/api/loans/', data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Loan.objects.filter(user=user, book=book, status='active').exists()
        
        book.refresh_from_db()
        assert book.available_copies == 4
    
    def test_cannot_borrow_unavailable_book(self):
        """Test cannot borrow book when none available."""
        user = UserFactory()
        book = BookFactory(available_copies=0)
        self.client.force_authenticate(user=user)
        
        data = {'book_id': book.id}
        response = self.client.post('/api/loans/', data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_cannot_borrow_same_book_twice(self):
        """Test user cannot borrow the same book twice."""
        from django.utils import timezone
        from datetime import timedelta
        user = UserFactory()
        book = BookFactory(available_copies=5)
        self.client.force_authenticate(user=user)
        
        # First borrow
        Loan.objects.create(user=user, book=book, status='active', due_date=timezone.now() + timedelta(days=14))
        
        # Try to borrow again
        data = {'book_id': book.id}
        response = self.client.post('/api/loans/', data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_return_book(self):
        """Test returning a book."""
        user = UserFactory()
        book = BookFactory(available_copies=3)
        loan = Loan.objects.create(user=user, book=book, status='active')
        
        self.client.force_authenticate(user=user)
        
        response = self.client.post(f'/api/loans/{loan.id}/return/')
        
        assert response.status_code == status.HTTP_200_OK
        
        loan.refresh_from_db()
        assert loan.status == 'returned'
        assert loan.return_date is not None
        
        book.refresh_from_db()
        assert book.available_copies == 4
    
    def test_user_can_view_own_loans(self):
        """Test user can view their own loans."""
        user = UserFactory()
        LoanFactory.create_batch(3, user=user)
        LoanFactory.create_batch(2)  # Other user's loans
        
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/loans/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
    
    def test_admin_can_view_all_loans(self):
        """Test admin can view all loans."""
        admin = AdminUserFactory()
        LoanFactory.create_batch(5)
        
        self.client.force_authenticate(user=admin)
        response = self.client.get('/api/loans/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 5
    
    def test_regular_user_cannot_view_all_loans(self):
        """Test regular user cannot view all loans (should only see their own)."""
        user = UserFactory()
        other_user = UserFactory()
        # Create loans for other user
        LoanFactory.create_batch(3, user=other_user)
        # Create one for current user
        LoanFactory.create(user=user)
        
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/loans/')
        
        # User should only see their own loan, not all loans
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_admin_can_view_overdue_loans(self):
        """Test admin can view overdue loans."""
        admin = AdminUserFactory()
        
        # Create overdue loan
        user = UserFactory()
        book = BookFactory()
        Loan.objects.create(
            user=user,
            book=book,
            due_date=datetime.now() - timedelta(days=5),
            status='active'
        )
        
        self.client.force_authenticate(user=admin)
        response = self.client.get('/api/admin/loans/overdue/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1


@pytest.mark.django_db
class TestPaginationAndFiltering:
    """Test pagination and filtering functionality."""
    
    def setup_method(self):
        """Setup test client."""
        self.client = APIClient()
        # Clean up any existing data
        Book.objects.all().delete()
    
    def test_books_pagination(self):
        """Test book list pagination."""
        BookFactory.create_batch(25)
        
        response = self.client.get('/api/books/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 25
        assert len(response.data['results']) == 10  # Default page size
        assert response.data['next'] is not None
    
    def test_books_pagination_second_page(self):
        """Test accessing second page of books."""
        BookFactory.create_batch(25)
        
        response = self.client.get('/api/books/?page=2')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 10
    
    def test_filter_books_by_author(self):
        """Test filtering books by author."""
        BookFactory.create_batch(3, author='John Doe')
        BookFactory.create_batch(2, author='Jane Smith')
        
        response = self.client.get('/api/books/?author=John')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
