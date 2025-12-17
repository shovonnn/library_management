from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta

User = get_user_model()


class Book(models.Model):
    """
    Model representing a book in the library.
    """
    title = models.CharField(max_length=255, db_index=True)
    author = models.CharField(max_length=255, db_index=True)
    isbn = models.CharField(max_length=13, unique=True, db_index=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    page_count = models.IntegerField(validators=[MinValueValidator(1)])
    language = models.CharField(max_length=50, default='English')
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, db_index=True)
    total_copies = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    available_copies = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    cover_image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        indexes = [
            models.Index(fields=['title', 'author']),
            models.Index(fields=['isbn']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    @property
    def is_available(self):
        """Check if the book is available for borrowing."""
        return self.available_copies > 0
    
    def save(self, *args, **kwargs):
        """Override save to ensure available_copies doesn't exceed total_copies."""
        if self.available_copies > self.total_copies:
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)


class Loan(models.Model):
    """
    Model representing a book loan transaction.
    """
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    borrowed_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-borrowed_date']
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['book', 'status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"
    
    def save(self, *args, **kwargs):
        """Set due date if not provided (14 days from now)."""
        if not self.due_date:
            self.due_date = datetime.now() + timedelta(days=14)
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        """Check if the loan is overdue."""
        if self.status == 'returned':
            return False
        from django.utils import timezone
        return timezone.now() > self.due_date
    
    @property
    def days_overdue(self):
        """Calculate days overdue."""
        if not self.is_overdue:
            return 0
        from django.utils import timezone
        return (timezone.now() - self.due_date).days
