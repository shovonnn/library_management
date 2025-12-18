import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from factories import UserFactory, AdminUserFactory

User = get_user_model()


@pytest.mark.django_db
class TestAuthenticationAPI:
    """Test cases for authentication endpoints."""
    
    def setup_method(self):
        """Setup test client."""
        self.client = APIClient()
        # Clean up any existing data  
        User.objects.all().delete()
    
    def test_user_registration(self):
        """Test user registration."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post('/api/auth/register/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data
        assert User.objects.filter(username='newuser').exists()
    
    def test_registration_password_mismatch(self):
        """Test registration with mismatched passwords."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPass123!',
            'password2': 'DifferentPass123!',
        }
        response = self.client.post('/api/auth/register/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_user_login(self):
        """Test user login."""
        user = UserFactory(username='testuser')
        user.set_password('testpass123')
        user.save()
        
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/login/', data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        data = {
            'username': 'nonexistent',
            'password': 'wrongpass'
        }
        response = self.client.post('/api/auth/login/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_user_profile(self):
        """Test retrieving user profile."""
        user = UserFactory()
        user.set_password('testpass')
        user.save()
        
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/auth/profile/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username
        assert response.data['email'] == user.email
    
    def test_update_user_profile(self):
        """Test updating user profile."""
        user = UserFactory()
        self.client.force_authenticate(user=user)
        
        data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        response = self.client.patch('/api/auth/profile/', data)
        
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.first_name == 'Updated'
        assert user.last_name == 'Name'
    
    def test_change_password(self):
        """Test changing password."""
        user = UserFactory()
        user.set_password('oldpass123')
        user.save()
        
        self.client.force_authenticate(user=user)
        
        data = {
            'old_password': 'oldpass123',
            'new_password': 'NewPass123!',
            'new_password2': 'NewPass123!'
        }
        response = self.client.post('/api/auth/change-password/', data)
        
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.check_password('NewPass123!')
    
    def test_admin_list_users(self):
        """Test admin listing all users."""
        admin = AdminUserFactory()
        UserFactory.create_batch(5)
        
        self.client.force_authenticate(user=admin)
        response = self.client.get('/api/auth/users/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 6  # 5 + admin
    
    def test_regular_user_cannot_list_users(self):
        """Test regular user cannot access user list."""
        user = UserFactory()
        self.client.force_authenticate(user=user)
        
        response = self.client.get('/api/auth/users/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
