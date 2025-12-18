import pytest
from django.contrib.auth import get_user_model
from accounts.models import User

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Test cases for User model."""
    
    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == 'user'
        assert user.is_active is True
        assert user.check_password('testpass123')
    
    def test_create_superuser(self):
        """Test creating a superuser."""
        admin = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@example.com',
            password='admin123'
        )
        assert admin.is_superuser is True
        assert admin.is_staff is True
        assert admin.is_admin is True
    
    def test_user_str_representation(self):
        """Test string representation of user."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        assert str(user) == 'testuser'
    
    def test_is_admin_property(self):
        """Test is_admin property."""
        regular_user = User.objects.create_user(
            username='regularuser2',
            email='regularuser2@example.com',
            password='pass123'
        )
        admin_user = User.objects.create_user(
            username='adminuser2',
            email='adminuser2@example.com',
            password='pass123',
            role='admin'
        )
        assert regular_user.is_admin is False
        assert admin_user.is_admin is True
