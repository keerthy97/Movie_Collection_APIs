# your_app/urls.py
from django.urls import path
from .views import register,paginated_movie_list,CollectionSummaryView, create_collection,handle_collection

urlpatterns = [
    path('register/', register, name='register'),                                              # for registering as a user
    path('movies/', paginated_movie_list, name='paginated_movie_list'),                        # get paginated list of movies 
    path('collections/', CollectionSummaryView.as_view(), name='collection-summary'),          # get collections
    path('collection/',create_collection,name='create_collection'),                            # post collections
    path('collection/<uuid:collection_uuid>/',handle_collection,name='handle_collection')      # put,get,delete collection with collection uuid
]
