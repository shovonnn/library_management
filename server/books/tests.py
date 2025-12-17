import pytest
from datetime import datetime, timedelta
from books.models import Book, Loan
from factories import BookFactory, UserFactory


@pytest.mark.django_db
class TestBookModel:
    """Test cases for Book model."""
    
    def test_create_book(self):
        """Test creating a book."""
        book = BookFactory()
        assert book.id is not None
        assert book.total_copies == 5
        assert book.available_copies == 5
    
    def test_book_str_representation(self):
        """Test string representation of book."""
        book = BookFactory(title='Test Book', author='Test Author')
        assert str(book) == 'Test Book by Test Author'
    
    def test_book_is_available(self):
        """Test book availability property."""
        book = BookFactory(available_copies=2)
        assert book.is_available is True
        
        book.available_copies = 0
        book.save()
        assert book.is_available is False
    
    def test_available_copies_validation(self):
        """Test that available copies cannot exceed total copies."""
        book = BookFactory(total_copies=5, available_copies=10)
        book.save()
        assert book.available_copies == book.total_copies


@pytest.mark.django_db
class TestLoanModel:
    """Test cases for Loan model."""
    
    def test_create_loan(self):
        """Test creating a loan."""
        user = UserFactory()
        book = BookFactory()
        loan = Loan.objects.create(
            user=user,
            book=book
        )
        assert loan.id is not None
        assert loan.status == 'active'
        assert loan.due_date is not None
    
    def test_loan_str_representation(self):
        """Test string representation of loan."""
        user = UserFactory(username='testuser')
        book = BookFactory(title='Test Book')
        loan = Loan.objects.create(user=user, book=book)
        assert 'testuser' in str(loan)
        assert 'Test Book' in str(loan)
    
    def test_loan_automatic_due_date(self):
        """Test that due date is automatically set."""
        user = UserFactory()
        book = BookFactory()
        loan = Loan.objects.create(user=user, book=book)
        
        expected_due_date = datetime.now() + timedelta(days=14)
        assert loan.due_date.date() == expected_due_date.date()
    
    def test_loan_is_overdue(self):
        """Test overdue detection."""
        user = UserFactory()
        book = BookFactory()
        
        # Not overdue
        loan = Loan.objects.create(
            user=user,
            book=book,
            due_date=datetime.now() + timedelta(days=1)
        )
        assert loan.is_overdue is False
        
        # Overdue
        overdue_loan = Loan.objects.create(
            user=user,
            book=book,
            due_date=datetime.now() - timedelta(days=1)
        )
        assert overdue_loan.is_overdue is True
    
    def test_returned_loan_not_overdue(self):
        """Test that returned loans are not marked as overdue."""
        user = UserFactory()
        book = BookFactory()
        loan = Loan.objects.create(
            user=user,
            book=book,
            due_date=datetime.now() - timedelta(days=5),
            status='returned'
        )
        assert loan.is_overdue is False
