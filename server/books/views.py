from rest_framework import generics, status, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from datetime import datetime, timedelta

from .models import Book, Loan
from .serializers import (
    BookSerializer, BookListSerializer, LoanSerializer, 
    LoanListSerializer, BorrowBookSerializer, ReturnBookSerializer
)
from .filters import BookFilter, LoanFilter
from .permissions import IsAdminOrReadOnly
from accounts.permissions import IsAdmin


class BookListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating books.
    GET: Anonymous users can view (read-only)
    POST: Admin only
    """
    queryset = Book.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookListSerializer
        return BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting books.
    GET: All users
    PUT/PATCH/DELETE: Admin only
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)


class LoanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing loans.
    """
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LoanFilter
    
    def get_queryset(self):
        """
        Admins see all loans, regular users see only their own.
        """
        if self.request.user.role == 'admin':
            return Loan.objects.all()
        return Loan.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """
        Borrow a book (POST /api/loans/)
        """
        book_id = request.data.get('book_id')
        
        if not book_id:
            return Response(
                {'error': 'book_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            book = Book.objects.get(id=book_id)
            
            # Check if book is available
            if book.available_copies <= 0:
                return Response(
                    {'error': 'This book is currently not available.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if user already has an active loan for this book
            active_loan = Loan.objects.filter(
                user=request.user,
                book=book,
                status__in=['borrowed', 'overdue']
            ).first()
            
            if active_loan:
                return Response(
                    {'error': 'You already have an active loan for this book.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create loan
            from django.utils import timezone
            loan = Loan.objects.create(
                user=request.user,
                book=book,
                due_date=timezone.now() + timedelta(days=14)
            )
            
            # Update book availability
            book.available_copies -= 1
            book.save()
            
            return Response(
                LoanSerializer(loan).data,
                status=status.HTTP_201_CREATED
            )
        
        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """
        Return a book (POST /api/loans/{id}/return/)
        """
        try:
            loan = self.get_object()
            
            # Check if loan belongs to user (unless admin)
            if request.user.role != 'admin' and loan.user != request.user:
                return Response(
                    {'error': 'You do not have permission to return this loan.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if already returned
            if loan.status == 'returned':
                return Response(
                    {'error': 'This book has already been returned.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update loan
            from django.utils import timezone
            loan.return_date = timezone.now()
            loan.status = 'returned'
            loan.save()
            
            # Update book availability
            book = loan.book
            book.available_copies += 1
            book.save()
            
            return Response(
                LoanSerializer(loan).data,
                status=status.HTTP_200_OK
            )
        
        except Loan.DoesNotExist:
            return Response(
                {'error': 'Loan not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def my_loans(self, request):
        """
        Get current user's loans (GET /api/loans/my-loans/)
        """
        status_filter = request.query_params.get('status')
        queryset = Loan.objects.filter(user=request.user)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        queryset = queryset.order_by('-borrowed_date')
        
        # Paginate
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = LoanSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = LoanSerializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'next': None,
            'previous': None,
            'results': serializer.data
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_books(request):
    """
    API endpoint for searching books by title, author, ISBN, or category.
    """
    query = request.query_params.get('q', '')
    
    if not query:
        return Response(
            {'error': 'Search query parameter "q" is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    books = Book.objects.filter(
        Q(title__icontains=query) |
        Q(author__icontains=query) |
        Q(isbn__icontains=query) |
        Q(category__icontains=query) |
        Q(description__icontains=query)
    )
    
    serializer = BookListSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdmin])
def overdue_loans(request):
    """
    API endpoint for viewing overdue loans (admin only).
    """
    loans = Loan.objects.filter(
        status='active',
        due_date__lt=datetime.now()
    )
    
    # Update status to overdue
    for loan in loans:
        loan.status = 'overdue'
        loan.save()
    
    serializer = LoanListSerializer(loans, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def book_categories(request):
    """
    API endpoint for getting all unique book categories.
    """
    categories = Book.objects.values_list('category', flat=True).distinct().order_by('category')
    return Response(list(categories))
