"""
Sample data creation script for testing the Library Management System.
Run this script to populate the database with sample books and users.

Usage:
    python create_sample_data.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from books.models import Book
from datetime import date

User = get_user_model()


def create_users():
    """Create sample users."""
    print("Creating sample users...")
    
    users_data = [
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'Password123!',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'user',
            'phone_number': '+1234567890',
            'address': '123 Main St, New York, NY'
        },
        {
            'username': 'jane_smith',
            'email': 'jane@example.com',
            'password': 'Password123!',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'role': 'user',
            'phone_number': '+1234567891',
            'address': '456 Oak Ave, Boston, MA'
        },
        {
            'username': 'bob_wilson',
            'email': 'bob@example.com',
            'password': 'Password123!',
            'first_name': 'Bob',
            'last_name': 'Wilson',
            'role': 'user',
            'phone_number': '+1234567892',
            'address': '789 Pine Rd, Chicago, IL'
        },
    ]
    
    created_count = 0
    for user_data in users_data:
        username = user_data.pop('username')
        password = user_data.pop('password')
        
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password, **user_data)
            created_count += 1
            print(f"  ✓ Created user: {username}")
        else:
            print(f"  - User already exists: {username}")
    
    print(f"Created {created_count} new users.\n")


def create_books():
    """Create sample books."""
    print("Creating sample books...")
    
    books_data = [
        {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'isbn': '9780743273565',
            'publisher': 'Scribner',
            'publication_date': date(1925, 4, 10),
            'page_count': 180,
            'language': 'English',
            'description': 'A classic American novel set in the Jazz Age that tells the story of Jay Gatsby and his obsession with Daisy Buchanan.',
            'category': 'Fiction',
            'total_copies': 5,
            'available_copies': 5,
        },
        {
            'title': '1984',
            'author': 'George Orwell',
            'isbn': '9780451524935',
            'publisher': 'Signet Classic',
            'publication_date': date(1949, 6, 8),
            'page_count': 328,
            'language': 'English',
            'description': 'A dystopian social science fiction novel and cautionary tale about totalitarianism.',
            'category': 'Science Fiction',
            'total_copies': 8,
            'available_copies': 8,
        },
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'isbn': '9780061120084',
            'publisher': 'Harper Perennial',
            'publication_date': date(1960, 7, 11),
            'page_count': 324,
            'language': 'English',
            'description': 'A novel about racial injustice and childhood innocence in the American South.',
            'category': 'Fiction',
            'total_copies': 6,
            'available_copies': 6,
        },
        {
            'title': 'Pride and Prejudice',
            'author': 'Jane Austen',
            'isbn': '9780141439518',
            'publisher': 'Penguin Classics',
            'publication_date': date(1813, 1, 28),
            'page_count': 432,
            'language': 'English',
            'description': 'A romantic novel of manners that critiques the British landed gentry at the end of the 18th century.',
            'category': 'Romance',
            'total_copies': 4,
            'available_copies': 4,
        },
        {
            'title': 'The Hobbit',
            'author': 'J.R.R. Tolkien',
            'isbn': '9780547928227',
            'publisher': 'Houghton Mifflin Harcourt',
            'publication_date': date(1937, 9, 21),
            'page_count': 310,
            'language': 'English',
            'description': 'A fantasy novel about the adventures of Bilbo Baggins.',
            'category': 'Fantasy',
            'total_copies': 7,
            'available_copies': 7,
        },
        {
            'title': 'Harry Potter and the Philosopher\'s Stone',
            'author': 'J.K. Rowling',
            'isbn': '9780747532699',
            'publisher': 'Bloomsbury',
            'publication_date': date(1997, 6, 26),
            'page_count': 223,
            'language': 'English',
            'description': 'The first novel in the Harry Potter series about a young wizard discovering his magical heritage.',
            'category': 'Fantasy',
            'total_copies': 10,
            'available_copies': 10,
        },
        {
            'title': 'The Catcher in the Rye',
            'author': 'J.D. Salinger',
            'isbn': '9780316769174',
            'publisher': 'Little, Brown and Company',
            'publication_date': date(1951, 7, 16),
            'page_count': 277,
            'language': 'English',
            'description': 'A novel about teenage rebellion and alienation.',
            'category': 'Fiction',
            'total_copies': 5,
            'available_copies': 5,
        },
        {
            'title': 'The Lord of the Rings',
            'author': 'J.R.R. Tolkien',
            'isbn': '9780544003415',
            'publisher': 'Houghton Mifflin Harcourt',
            'publication_date': date(1954, 7, 29),
            'page_count': 1178,
            'language': 'English',
            'description': 'An epic high-fantasy novel about the quest to destroy the One Ring.',
            'category': 'Fantasy',
            'total_copies': 6,
            'available_copies': 6,
        },
        {
            'title': 'Animal Farm',
            'author': 'George Orwell',
            'isbn': '9780451526342',
            'publisher': 'Signet Classic',
            'publication_date': date(1945, 8, 17),
            'page_count': 112,
            'language': 'English',
            'description': 'A satirical allegorical novella about totalitarianism.',
            'category': 'Political Fiction',
            'total_copies': 8,
            'available_copies': 8,
        },
        {
            'title': 'Brave New World',
            'author': 'Aldous Huxley',
            'isbn': '9780060850524',
            'publisher': 'Harper Perennial',
            'publication_date': date(1932, 1, 1),
            'page_count': 311,
            'language': 'English',
            'description': 'A dystopian novel set in a futuristic World State.',
            'category': 'Science Fiction',
            'total_copies': 5,
            'available_copies': 5,
        },
        {
            'title': 'The Chronicles of Narnia',
            'author': 'C.S. Lewis',
            'isbn': '9780066238500',
            'publisher': 'HarperCollins',
            'publication_date': date(1950, 10, 16),
            'page_count': 767,
            'language': 'English',
            'description': 'A series of seven fantasy novels about the magical land of Narnia.',
            'category': 'Fantasy',
            'total_copies': 4,
            'available_copies': 4,
        },
        {
            'title': 'Moby-Dick',
            'author': 'Herman Melville',
            'isbn': '9780142437247',
            'publisher': 'Penguin Classics',
            'publication_date': date(1851, 10, 18),
            'page_count': 585,
            'language': 'English',
            'description': 'A novel about the voyage of the whaling ship Pequod.',
            'category': 'Adventure',
            'total_copies': 3,
            'available_copies': 3,
        },
        {
            'title': 'The Odyssey',
            'author': 'Homer',
            'isbn': '9780140268867',
            'publisher': 'Penguin Classics',
            'publication_date': date(1800, 1, 1),
            'page_count': 541,
            'language': 'English',
            'description': 'An ancient Greek epic poem about the hero Odysseus.',
            'category': 'Epic Poetry',
            'total_copies': 4,
            'available_copies': 4,
        },
        {
            'title': 'War and Peace',
            'author': 'Leo Tolstoy',
            'isbn': '9780143039990',
            'publisher': 'Penguin Classics',
            'publication_date': date(1869, 1, 1),
            'page_count': 1225,
            'language': 'English',
            'description': 'A historical novel that chronicles French invasion of Russia.',
            'category': 'Historical Fiction',
            'total_copies': 3,
            'available_copies': 3,
        },
        {
            'title': 'The Divine Comedy',
            'author': 'Dante Alighieri',
            'isbn': '9780142437223',
            'publisher': 'Penguin Classics',
            'publication_date': date(1320, 1, 1),
            'page_count': 798,
            'language': 'English',
            'description': 'An epic poem describing Dante\'s journey through Hell, Purgatory, and Paradise.',
            'category': 'Epic Poetry',
            'total_copies': 2,
            'available_copies': 2,
        },
    ]
    
    created_count = 0
    for book_data in books_data:
        isbn = book_data['isbn']
        
        if not Book.objects.filter(isbn=isbn).exists():
            Book.objects.create(**book_data)
            created_count += 1
            print(f"  ✓ Created book: {book_data['title']}")
        else:
            print(f"  - Book already exists: {book_data['title']}")
    
    print(f"Created {created_count} new books.\n")


def main():
    print("=" * 60)
    print("Library Management System - Sample Data Creator")
    print("=" * 60)
    print()
    
    # Create admin if doesn't exist
    if not User.objects.filter(username='admin').exists():
        print("Creating admin user...")
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin'
        )
        print("  ✓ Created admin user (username: admin, password: admin123)\n")
    else:
        print("Admin user already exists.\n")
    
    # Create sample data
    create_users()
    create_books()
    
    # Summary
    print("=" * 60)
    print("Summary:")
    print("=" * 60)
    print(f"Total Users: {User.objects.count()}")
    print(f"Total Books: {Book.objects.count()}")
    print(f"Available Books: {Book.objects.filter(available_copies__gt=0).count()}")
    print()
    print("Sample Data Created Successfully!")
    print()
    print("You can now:")
    print("  - Login as admin (username: admin, password: admin123)")
    print("  - Login as regular user (username: john_doe, password: Password123!)")
    print("  - Browse and borrow books")
    print("=" * 60)


if __name__ == '__main__':
    main()
