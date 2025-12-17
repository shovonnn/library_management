import factory
from factory.django import DjangoModelFactory
from faker import Faker
from accounts.models import User
from books.models import Book, Loan
from datetime import datetime, timedelta

fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone_number = factory.Faker('phone_number')
    address = factory.Faker('address')
    role = 'user'
    is_active = True


class AdminUserFactory(UserFactory):
    role = 'admin'
    is_staff = True


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book
    
    title = factory.Faker('sentence', nb_words=4)
    author = factory.Faker('name')
    isbn = factory.Sequence(lambda n: f'978{n:010d}')
    publisher = factory.Faker('company')
    publication_date = factory.Faker('date_between', start_date='-10y', end_date='today')
    page_count = factory.Faker('random_int', min=50, max=1000)
    language = 'English'
    description = factory.Faker('text')
    category = factory.Faker('word')
    total_copies = 5
    available_copies = 5


class LoanFactory(DjangoModelFactory):
    class Meta:
        model = Loan
    
    user = factory.SubFactory(UserFactory)
    book = factory.SubFactory(BookFactory)
    borrowed_date = factory.LazyFunction(datetime.now)
    due_date = factory.LazyFunction(lambda: datetime.now() + timedelta(days=14))
    status = 'active'
