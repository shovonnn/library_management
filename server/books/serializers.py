from rest_framework import serializers
from .models import Book, Loan
from accounts.serializers import UserSerializer


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model."""
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def validate(self, attrs):
        """Validate that available_copies doesn't exceed total_copies."""
        total_copies = attrs.get('total_copies', self.instance.total_copies if self.instance else None)
        available_copies = attrs.get('available_copies', self.instance.available_copies if self.instance else None)
        
        if total_copies and available_copies and available_copies > total_copies:
            raise serializers.ValidationError(
                "Available copies cannot exceed total copies."
            )
        return attrs


class BookListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing books."""
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'isbn', 'category', 
                  'available_copies', 'total_copies', 'is_available')


class LoanSerializer(serializers.ModelSerializer):
    """Serializer for Loan model."""
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), 
        source='book', 
        write_only=True
    )
    is_overdue = serializers.ReadOnlyField()
    days_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ('user', 'borrowed_date', 'status')
    
    def validate_book_id(self, value):
        """Validate that the book is available for borrowing."""
        if not value.is_available:
            raise serializers.ValidationError(
                "This book is currently not available for borrowing."
            )
        return value


class LoanListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing loans."""
    user_username = serializers.CharField(source='user.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Loan
        fields = ('id', 'user_username', 'book_title', 'borrowed_date', 
                  'due_date', 'return_date', 'status', 'is_overdue')


class BorrowBookSerializer(serializers.Serializer):
    """Serializer for borrowing a book."""
    book_id = serializers.IntegerField()
    due_date = serializers.DateTimeField(required=False)
    
    def validate_book_id(self, value):
        """Validate that the book exists and is available."""
        try:
            book = Book.objects.get(id=value)
            if not book.is_available:
                raise serializers.ValidationError("This book is not available for borrowing.")
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found.")
        return value


class ReturnBookSerializer(serializers.Serializer):
    """Serializer for returning a book."""
    loan_id = serializers.IntegerField()
    notes = serializers.CharField(required=False, allow_blank=True)
