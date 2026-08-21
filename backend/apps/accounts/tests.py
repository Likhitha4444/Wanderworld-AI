from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import User
from django.contrib.auth.hashers import check_password

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.me_url = reverse('me')
        self.token_refresh_url = reverse('token_refresh')
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'StrongPassword123!',
            'password_confirmation': 'StrongPassword123!',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_registration_valid(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='testuser@example.com').exists())

    def test_duplicate_email(self):
        User.objects.create_user(email='testuser@example.com', password='password123')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_role_injection(self):
        data = self.user_data.copy()
        data['role'] = 'ADMIN'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email='testuser@example.com')
        self.assertEqual(user.role, 'USER')

    def test_password_hashed(self):
        self.client.post(self.register_url, self.user_data, format='json')
        user = User.objects.get(email='testuser@example.com')
        self.assertNotEqual(user.password, 'StrongPassword123!')
        self.assertTrue(check_password('StrongPassword123!', user.password))

    def test_password_not_in_response(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertNotIn('password', response.data['data'])

    def test_login_valid(self):
        User.objects.create_user(email='loginuser@example.com', password='password123')
        response = self.client.post(self.login_url, {'email': 'loginuser@example.com', 'password': 'password123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])
        self.assertIn('user', response.data['data'])

    def test_login_wrong_password(self):
        User.objects.create_user(email='loginuser@example.com', password='password123')
        response = self.client.post(self.login_url, {'email': 'loginuser@example.com', 'password': 'wrongpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_authenticated(self):
        user = User.objects.create_user(email='authuser@example.com', password='password123')
        self.client.force_authenticate(user=user)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], 'authuser@example.com')

    def test_me_unauthenticated(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_inactive_user_login(self):
        user = User.objects.create_user(email='inactive@example.com', password='password123', is_active=False)
        response = self.client.post(self.login_url, {'email': 'inactive@example.com', 'password': 'password123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ProfileAndSecurityTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='Password123!')
        self.user_profile_url = reverse('profile')
        self.change_password_url = reverse('change_password')
        self.logout_url = reverse('logout')

    def test_profile_get_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('bio', response.data['data'])

    def test_profile_patch_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {'bio': 'New bio'}
        response = self.client.patch(self.user_profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'New bio')

    def test_change_password_valid(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'current_password': 'Password123!',
            'new_password': 'NewPassword123!',
            'new_password_confirmation': 'NewPassword123!'
        }
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password('NewPassword123!'))

    def test_change_password_wrong_current(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'current_password': 'WrongPassword!',
            'new_password': 'NewPassword123!',
            'new_password_confirmation': 'NewPassword123!'
        }
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
