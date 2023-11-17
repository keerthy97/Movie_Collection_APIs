Backend Assignment
Introduction
This repository contains a Django web application that integrates with a movie listing API, implements APIs for managing movie collections, and includes a scalable request counter middleware. The goal is to assess your understanding of various concepts required for building a resilient Django project that handles concurrent requests.

To submit your assignment, push your code to GitHub and share the repository link with us. You have three days from receiving the assignment to complete it.

Evaluation Criteria
We will evaluate your assignment based on the following criteria:

Does your code fulfill the assignment requirements?
Is your code clean and modular, following PEP8 code formatting guidelines?
Does your counter implementation work in parallel execution of code?
Have you followed Django development best practices?
Have you added tests for your code, using Factory Boy for generating fixtures, with meaningful assertions?
Is your requirements file updated with all requirements?
Movie Listing API Integration
Endpoint: GET /movies/
Retrieve a paginated list of movies from a third-party API. The response includes movie details such as title, description, genres, and a unique UUID.

Web Application APIs
User Registration
Endpoint: POST /register/
Register a user with a desired username and password.
Response includes an access token.
Collection Management
Endpoint: GET /collections/

Retrieve user collections and top 3 favorite genres based on movies across all collections.
Endpoint: POST /collections/

Create a collection with a specified title, description, and list of movies.
Endpoint: PUT /collections/<collection_uuid>/

Update the movie list in a collection.
Endpoint: GET /collections/<collection_uuid>/

Retrieve details of a specific collection.
Endpoint: DELETE /collections/<collection_uuid>/

Delete a collection.
Request Counter Middleware
Endpoint: GET /request-count/
Retrieve the number of requests served by the server.

Endpoint: POST /request-count/reset/
Reset the request count.

Getting Started
Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/backend-assignment.git
cd backend-assignment
Set Up Virtual Environment:

bash
Copy code
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Set Environment Variables:

Copy the provided sample environment file:
bash
Copy code
cp .env.example .env
Open the .env file and replace placeholders with your API credentials.
Run Migrations:

bash
Copy code
python manage.py migrate
Run the Development Server:

bash
Copy code
python manage.py runserver
The server will be accessible at http://localhost:8000/.