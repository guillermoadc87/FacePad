from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path(r'api-token-auth/', obtain_auth_token),
    path(r'register/', views.register),
    path(r'example/', views.example_view)
]