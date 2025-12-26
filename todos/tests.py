from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token

from todos.models import ToDo


# Create your tests here.
class TestTodo(TestCase):
    user = None

    def create_token(self):
        self.user = User.objects.create_user('clive@rosfield.test', 'password123')
        return Token.objects.get_or_create(user=self.user)[0].key

    def create_todo(self):
        title = 'Basic attack commands'
        description = 'Learn the basis of attack commands execution'
        return ToDo.objects.create(title=title, description=description, user=self.user)

    def test_create_success(self):
        path = reverse('todos:index')
        response = self.client.post(path, {
            'title': 'Basic attack commands',
            'description': 'Learn the basis of attack commands execution'
        }, content_type='application/json', headers={
            'Authorization': 'Token ' + self.create_token()
        })
        self.assertEqual(response.status_code, 201)

    def test_create_without_token(self):
        path = reverse('todos:index')
        response = self.client.post(path, {
            'title': 'Basic attack commands',
            'description': 'Learn the basis of attack commands execution'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_create_invalid_method(self):
        path = reverse('todos:index')
        response = self.client.delete(path, {
            'title': 'Basic attack commands',
            'description': 'Learn the basis of attack commands execution'
        }, content_type='application/json', headers={
            'Authorization': 'Token ' + self.create_token()
        })
        self.assertEqual(response.status_code, 405)

    def test_create_without_title(self):
        path = reverse('todos:index')
        response = self.client.post(path, {
            'description': 'Learn the basis of attack commands execution'
        }, content_type='application/json', headers={
            'Authorization': 'Token ' + self.create_token()
        })
        self.assertEqual(response.status_code, 400)

    def test_create_with_long_title(self):
        path = reverse('todos:index')
        response = self.client.post(path, {
            'title': 'Basic attack commands' * 128,
            'description': 'Learn the basis of attack commands execution'
        }, content_type='application/json', headers={
            'Authorization': 'Token ' + self.create_token()
        })
        self.assertEqual(response.status_code, 400)

    def test_create_without_description(self):
        path = reverse('todos:index')
        response = self.client.post(path, {
            'title': 'Basic attack commands',
        }, content_type='application/json', headers={
            'Authorization': 'Token ' + self.create_token()
        })
        self.assertEqual(response.status_code, 400)

    def test_create_with_long_description(self):
        path = reverse('todos:index')
        response = self.client.post(path, {
            'title': 'Basic attack commands',
            'description': 'Learn the basis of attack commands execution' * 1024
        }, content_type='application/json', headers={
            'Authorization': 'Token ' + self.create_token()
        })
        self.assertEqual(response.status_code, 400)

    def test_update_success(self):
        token = self.create_token()
        todo = self.create_todo()
        path = reverse('todos:item', args=[todo.id])
        response = self.client.put(path, {
            'title': 'Basic magic commands',
            'description': 'Learn the basis of magic commands execution'
        }, content_type='application/json', headers={
            'Authorization': 'Token ' + token
        })
        self.assertEqual(response.status_code, 200)

    def test_update_without_token(self):
        self.create_token()
        todo = self.create_todo()
        path = reverse('todos:item', args=[todo.id])
        response = self.client.put(path, {
            'title': 'Basic magic commands',
            'description': 'Learn the basis of magic commands execution'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_update_invalid_method(self):
        token = self.create_token()
        todo = self.create_todo()
        path = reverse('todos:item', args=[todo.id])
        response = self.client.post(path, {
            'title': 'Basic magic commands',
            'description': 'Learn the basis of magic commands execution'
        }, content_type='application/json', headers={
            'Authorization': 'Token ' + token
        })
        self.assertEqual(response.status_code, 405)

    def test_update_not_found(self):
        token = self.create_token()
        self.create_todo()
        path = reverse('todos:item', args=[9999])
        response = self.client.put(path, {
            'title': 'Basic magic commands',
            'description': 'Learn the basis of magic commands execution'
        }, content_type='application/json', headers={
            'Authorization': 'Token ' + token
        })
        self.assertEqual(response.status_code, 404)
