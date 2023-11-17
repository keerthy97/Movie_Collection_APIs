# Backend Assignment

## Introduction

This repository contains a Django web application that integrates with a movie listing API, implements APIs for managing movie collections, and includes a scalable request counter middleware. The goal is to assess your understanding of various concepts required for building a resilient Django project that handles concurrent requests.

## Getting Started

1. **Clone the Repository:**
    [repo](https://github.com/keerthy97/Movie_Collection_APIs)
   
2. **Set Up Virtual Environment:**
   ```bash python -m venv venv
3. **Install Dependencies:**
    ```bash pip install -r requirements.txt
4. **Set Environment Variables:**
   Copy user name and password from environment file:

5. **Run Migrations:**
    ```bash python manage.py migrate
    
6. **Run the Development Server:**
    ```bash python manage.py runserver
The server will be accessible at http://localhost:8000/.

## Movie Listing API Integration

**Endpoint: GET /movies/**

Retrieve a paginated list of movies from a third-party API. The response includes movie details such as title, description, genres, and a unique UUID.

## Web Application APIs

### User Registration

**Endpoint: POST /register/**

Register a user with a desired username and password. Response includes an access token.

### Collection Management

**Endpoint: GET /collections/**

Retrieve user collections and top 3 favorite genres based on movies across all collections.

**Endpoint: POST /collections/**

Create a collection with a specified title, description, and list of movies.

**Endpoint: PUT /collections/<collection_uuid>/**

Update the movie list in a collection.

**Endpoint: GET /collections/<collection_uuid>/**

Retrieve details of a specific collection.

**Endpoint: DELETE /collections/<collection_uuid>/**

Delete a collection.

## Request Counter Middleware

**Endpoint: GET /request-count/**

Retrieve the number of requests served by the server.

**Endpoint: POST /request-count/reset/**

Reset the request count.









