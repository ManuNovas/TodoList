from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class TestUsers(TestCase):
    def create_user(self):
        return User.objects.create_user(username='clive@rosfield.test', password='password123')

    def test_register_success(self):
        response = self.client.post(reverse('users:register'), {
            'name': 'Clive Rosfield',
            'email': 'clive@rosfield.test',
            'password': 'password123',
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def test_register_long_name(self):
        response = self.client.post(reverse('users:register'), {
            'name': 'Clive Rosfield ' * 128,
            'email': 'cliver@rosfield.test',
            'password': 'password123'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.json())

    def test_register_without_name(self):
        response = self.client.post(reverse('users:register'), {
            'email': 'cliver@rosfield.test',
            'password': 'password123'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.json())

    def test_register_invalid_email(self):
        response = self.client.post(reverse('users:register'), {
            'name': 'Clive Rosfield',
            'email': 'rosfield.test',
            'password': 'password123'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json())

    def test_register_long_email(self):
        response = self.client.post(reverse('users:register'), {
            'name': 'Clive Rosfield',
            'email': ('clive' * 128) + '@rosfield.test',
            'password': 'password123'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json())

    def test_register_without_email(self):
        response = self.client.post(reverse('users:register'), {
            'name': 'Clive Rosfield',
            'password': 'password123'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json())

    def test_register_existing_email(self):
        self.create_user()
        response = self.client.post(reverse('users:register'), {
            'name': 'Clive Rosfield',
            'email': 'clive@rosfield.test',
            'password': 'password123',
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json())

    def test_register_long_password(self):
        response = self.client.post(reverse('users:register'), {
            'name': 'Clive Rosfield',
            'email': 'clive@rosfield.test',
            'password': 'password123' * 128
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.json())

    def test_register_without_password(self):
        response = self.client.post(reverse('users:register'), {
            'name': 'Clive Rosfield',
            'email': 'clive@rosfield.test'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.json())
