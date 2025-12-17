from django.contrib import admin
from .models import Book, Loan


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'available_copies', 'total_copies', 'created_at')
    list_filter = ('category', 'language', 'created_at')
    search_fields = ('title', 'author', 'isbn', 'category')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'isbn', 'publisher', 'publication_date')
        }),
        ('Details', {
            'fields': ('page_count', 'language', 'category', 'description', 'cover_image')
        }),
        ('Availability', {
            'fields': ('total_copies', 'available_copies')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_date', 'due_date', 'return_date', 'status')
    list_filter = ('status', 'borrowed_date', 'due_date')
    search_fields = ('user__username', 'user__email', 'book__title', 'book__isbn')
    readonly_fields = ('borrowed_date',)
    ordering = ('-borrowed_date',)
    
    fieldsets = (
        ('Loan Information', {
            'fields': ('user', 'book', 'borrowed_date', 'due_date', 'return_date', 'status')
        }),
        ('Additional Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return self.readonly_fields + ('user', 'book')
        return self.readonly_fields
