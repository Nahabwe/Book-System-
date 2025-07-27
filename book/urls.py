from .views import *
from django.urls import path


urlpatterns=[
    path('author/',author_list),
    path('author-details/<int:pk>/',author_details),
    path('genre/',genre_list),
    path('genre-details/<int:pk>/',genre_details),
    path('book/',book_list),
    path('book-details/<int:pk>/',book_details),
    path('review/',review_list),
    path('review-details/<int:pk>/',review_details),
]