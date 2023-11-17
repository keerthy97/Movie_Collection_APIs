import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from .models import Movie, Collection, MovieCollection
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', 'password123')

class MovieFactory(DjangoModelFactory):
    class Meta:
        model = Movie

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    genres = factory.Faker('word')

class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = Collection

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    user = factory.SubFactory(UserFactory)

class MovieCollectionFactory(DjangoModelFactory):
    class Meta:
        model = MovieCollection

    collection = factory.SubFactory(CollectionFactory)
    movie = factory.SubFactory(MovieFactory)

class CollectionTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = UserFactory()

        # Create a test movie
        self.movie = MovieFactory()

        # Create a test collection
        self.collection = CollectionFactory(user=self.user)
        self.collection.movies.add(self.movie)

        # Set up the client for making API requests
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_collection(self):
        # Use the factories to generate fake data
        user = UserFactory()
        movie = MovieFactory()
        
        # Create a collection with the generated data
        data = {
            'title': 'Test Collection',
            'description': 'Test Description',
            'movies': [{'title': 'Test Movie', 'description': 'Test Description', 'genres': 'Action'}],
            'user': user.id
        }

        response = self.client.post('/collection/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class CollectionTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = UserFactory()

        # Create a test movie
        self.movie = MovieFactory()

        # Create a test collection
        self.collection = CollectionFactory(user=self.user)
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
        data = {
            'title': 'Updated Collection',
            'description': 'Updated Description',
            'movies': [{'title': 'Updated Movie', 'description': 'Updated Description', 'genres': 'Drama'}]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_collection(self):
        url = f'/collection/{self.collection.uuid}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Collection.objects.filter(uuid=self.collection.uuid).exists())
