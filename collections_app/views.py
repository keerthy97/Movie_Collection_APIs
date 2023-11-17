# views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Collection, Movie, User
from .serializers import CollectionResponseSerializer, CollectionSummarySerializer, CollectionCreateSerializer, CollectionDetailSerializer,CollectionUpdateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Count
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import get_top_favorite_genres, get_paginated_movie_list
from django.views.decorators.csrf import csrf_exempt
from collections import Counter
from collections_app.middleware import RequestCountMiddleware
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging


#register as a user with new user id and password 
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])  # Make sure AllowAny is used for registration
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user, created = User.objects.get_or_create(username=username)
    if not created:
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(password)
    user.save()

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return Response({
        'user' : user.id,
        'access_token': access_token,
        'refresh_token': refresh_token
    }, status=status.HTTP_201_CREATED)


#get paginated movies list from third party api from local host
logger = logging.getLogger(__name__)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def paginated_movie_list(request):
    page = request.query_params.get('page', 1)
    movies_data = get_paginated_movie_list(page)
    return Response({"movies_data": movies_data})


#get collections with favourite geners
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
class CollectionSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        collections = Collection.objects.filter(user=user)

        # Get top 3 genres across all user collections
        all_genres = []
        for collection in collections:
            all_genres.extend(collection.movies.values_list('genres', flat=True))

        genre_counts = Counter(all_genres)
        top_genres = [genre for genre, _ in genre_counts.most_common(3)]
        

        # Serialize collections without detailed movie information
        collection_serializer = CollectionSummarySerializer(collections, many=True)
        data = {
            'collections': collection_serializer.data,
            'favourite_genres': ', '.join(top_genres)
        }

        # Serialize the response
        response_serializer = CollectionResponseSerializer(data={'is_success': True, 'data': data})
        response_serializer.is_valid()

        return Response(response_serializer.data, status=status.HTTP_200_OK)


#create collection
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_collection(request):
    serializer = CollectionCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        collection_data = serializer.save(user=request.user)
        return Response({'is_success': True, 'data': {'collection_uuid': collection_data['collection_uuid']}}, status=status.HTTP_201_CREATED)
    return Response({'is_success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# put, get, delete collection with collection uuid
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def handle_collection(request, collection_uuid):
    try:
        collection = Collection.objects.get(uuid=collection_uuid, user=request.user)
    except Collection.DoesNotExist:
        return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CollectionDetailSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CollectionUpdateSerializer(collection, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"updated successfully"},status=status.HTTP_200_OK)
            # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        collection.delete()
        return Response({'message': 'Collection deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    # If an unsupported HTTP method is used
    return Response({'error': 'Unsupported HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# counter for request and response 
# views.py
def request_count(request):
    count = RequestCountMiddleware.get_request_count()
    return JsonResponse({'requests': count})

@csrf_exempt
def reset_request_count(request):
    RequestCountMiddleware.reset_request_count()
    return JsonResponse({'message': 'Request count reset successfully'})


# api view for refresh token
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def refresh_access_token(request):
    refresh_token = request.data.get('refresh')

    if not refresh_token:
        return Response({'error': 'Refresh token not provided'}, status=400)

    try:
        refresh_token = RefreshToken(refresh_token)
        access_token = str(refresh_token.access_token)
        return Response({'access_token': access_token})
    except Exception as e:
        return Response({'error': f'Error refreshing token: {str(e)}'}, status=400)
    

