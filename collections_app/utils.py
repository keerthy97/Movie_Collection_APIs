# movie_api/utils.py
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from rest_framework.response import Response
import logging
from collections import Counter

#fetching data from the third party api
def get_movie_list():
    url = 'https://demo.credy.in/api/v1/maya/movies/'
    username = os.getenv('MOVIE_API_USERNAME')
    password = os.getenv('MOVIE_API_PASSWORD')

    response = requests.get(url, auth=(username, password))
    response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

    return response.json()['data']


logger = logging.getLogger(__name__)

def get_paginated_movie_list(page=1):
    url = f'https://demo.credy.in/api/v1/maya/movies/?page={page}'
    username = os.getenv('MOVIE_API_USERNAME')
    password = os.getenv('MOVIE_API_PASSWORD')

    # Set your retry configuration
    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])

    # Use a session to apply the retry configuration
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        # Make the request to the third-party API with retries and disable SSL verification
        response = session.get(url, auth=(username, password), verify=False)
        response.raise_for_status()

        # Assuming the response is a JSON object with 'count', 'next', 'previous', and 'data' keys
        return response.json()
    except requests.RequestException as e:
        # Log the error
        logger.error(f"Failed to fetch movie data: {str(e)}")
        # Return a dictionary with an 'error' key
        return {'error': f"Failed to fetch movie data: {str(e)}"}
    
#utility function to get the top 3 favourite geners of the collection    
def get_top_favorite_genres(collections):
    all_genres = []
    
    # Collect all genres from movies in collections
    for collection in collections:
        for movie in collection.movies.all():
            all_genres.extend(movie.genres.split(','))

    # Calculate the top 3 favorite genres
    genre_counter = Counter(all_genres)
    top_genres = genre_counter.most_common(3)

    return [genre[0] for genre in top_genres]