from django.urls import path

from . import views

urlpatterns = [
    path(r'^api-token-auth/', views.obtain_auth_token)
]