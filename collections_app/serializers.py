# serializers.py
from rest_framework import serializers
from .models import Collection, Movie, MovieCollection


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class CollectionCreateSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies']

    def create(self, validated_data):
        movies_data = validated_data.pop('movies')
        collection = Collection.objects.create(**validated_data)

        for movie_data in movies_data:
            movie = Movie.objects.create(**movie_data)
            MovieCollection.objects.create(collection=collection, movie=movie)

        return {'collection_uuid': str(collection.uuid)}


class CollectionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title', 'uuid', 'description']


class CollectionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies']


class CollectionResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    data = serializers.DictField(child=CollectionSummarySerializer())


class CollectionDetailSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['title', 'uuid', 'description', 'movies']

