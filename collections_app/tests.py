from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Collection, Movie

class CollectionTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test movie
        self.movie = Movie.objects.create(title='Test Movie', description='Test Description', genres='Action')

        # Create a test collection
        self.collection = Collection.objects.create(title='Test Collection', description='Test Description', user=self.user)
        self.collection.movies.add(self.movie)

        # Set up the client for making API requests
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_collection(self):
        url = f'/collection/{self.collection.uuid}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_collection(self):
        url = f'/collection/{self.collection.uuid}/'
        data = {'title': 'Updated Collection', 'description': 'Updated Description', 'movies': [{'title': 'Updated Movie', 'description': 'Updated Description', 'genres': 'Drama'}]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_collection(self):
        url = f'/collection/{self.collection.uuid}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Collection.objects.filter(uuid=self.collection.uuid).exists())

