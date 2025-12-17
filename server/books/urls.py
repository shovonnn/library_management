from django.urls import path
from .views import (
    BookListCreateView, BookDetailView, LoanViewSet,
    search_books, overdue_loans, book_categories
)

urlpatterns = [
    # Books
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/search/', search_books, name='book-search'),
    path('books/categories/', book_categories, name='book-categories'),
    
    # Loans
    path('loans/', LoanViewSet.as_view({'get': 'list', 'post': 'create'}), name='loan-list-create'),
    path('loans/<int:pk>/', LoanViewSet.as_view({'get': 'retrieve'}), name='loan-detail'),
    path('loans/<int:pk>/return/', LoanViewSet.as_view({'post': 'return_book'}), name='loan-return'),
    path('loans/my-loans/', LoanViewSet.as_view({'get': 'my_loans'}), name='my-loans'),
    
    # Admin
    path('admin/loans/overdue/', overdue_loans, name='overdue-loans'),
]
