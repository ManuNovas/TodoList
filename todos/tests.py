from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token


# Create your tests here.
class TestTodo(TestCase):
    @staticmethod
    def create_token():
        user = User.objects.create_user('clive@rosfield.test', 'password123')
        return Token.objects.get_or_create(user=user)[0].key

    def test_create_success(self):
        response = self.client.post('/todos/', {
            'title': 'Basic attack commands',
            'description': 'Learn the basis of attack commands execution'
        }, content_type='application/json', headers={
            'Authorization': 'Token ' + self.create_token()
        })
        self.assertEqual(response.status_code, 201)

    def test_create_without_token(self):
        response = self.client.post('/todos/', {
            'title': 'Basic attack commands',
            'description': 'Learn the basis of attack commands execution'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_create_invalid_method(self):
        response = self.client.delete('/todos/', {
            'title': 'Basic attack commands',
            'description': 'Learn the basis of attack commands execution'
        }, content_type='application/json', headers={
            'Authorization': 'Token ' + self.create_token()
        })
        self.assertEqual(response.status_code, 405)

    def test_create_without_title(self):
        response = self.client.post('/todos/', {
            'description': 'Learn the basis of attack commands execution'
        }, content_type='application/json', headers={
            'Authorization': 'Token ' + self.create_token()
        })
        self.assertEqual(response.status_code, 400)

    def test_create_with_long_title(self):
        response = self.client.post('/todos/', {
            'title': 'Basic attack commands' * 128,
            'description': 'Learn the basis of attack commands execution'
        }, content_type='application/json', headers={
            'Authorization': 'Token ' + self.create_token()
        })
        self.assertEqual(response.status_code, 400)

    def test_create_without_description(self):
        response = self.client.post('/todos/', {
            'title': 'Basic attack commands',
        }, content_type='application/json', headers={
            'Authorization': 'Token ' + self.create_token()
        })
        self.assertEqual(response.status_code, 400)

    def test_crete_with_long_description(self):
        response = self.client.post('/todos/', {
            'title': 'Basic attack commands',
            'description': 'Learn the basis of attack commands execution' * 1024
        }, content_type='application/json', headers={
            'Authorization': 'Token ' + self.create_token()
        })
        self.assertEqual(response.status_code, 400)
