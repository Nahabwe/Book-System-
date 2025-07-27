from django.urls import path
from .views import *
urlpatterns=[
    path('register',register_user,name='register'),
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
]
