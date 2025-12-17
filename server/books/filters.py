from django_filters import rest_framework as filters
from .models import Book, Loan


class BookFilter(filters.FilterSet):
    """Filter for Book model."""
    title = filters.CharFilter(lookup_expr='icontains')
    author = filters.CharFilter(lookup_expr='icontains')
    category = filters.CharFilter(lookup_expr='icontains')
    language = filters.CharFilter(lookup_expr='icontains')
    available = filters.BooleanFilter(method='filter_available')
    min_pages = filters.NumberFilter(field_name='page_count', lookup_expr='gte')
    max_pages = filters.NumberFilter(field_name='page_count', lookup_expr='lte')
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'language', 'isbn']
    
    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(available_copies__gt=0)
        return queryset.filter(available_copies=0)


class LoanFilter(filters.FilterSet):
    """Filter for Loan model."""
    status = filters.ChoiceFilter(choices=Loan.STATUS_CHOICES)
    user = filters.NumberFilter(field_name='user__id')
    book = filters.NumberFilter(field_name='book__id')
    borrowed_after = filters.DateTimeFilter(field_name='borrowed_date', lookup_expr='gte')
    borrowed_before = filters.DateTimeFilter(field_name='borrowed_date', lookup_expr='lte')
    due_after = filters.DateTimeFilter(field_name='due_date', lookup_expr='gte')
    due_before = filters.DateTimeFilter(field_name='due_date', lookup_expr='lte')
    
    class Meta:
        model = Loan
        fields = ['status', 'user', 'book']
