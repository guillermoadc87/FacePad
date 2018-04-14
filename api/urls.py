from django.urls import path, re_path
from .serializers import CustomJWTSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from . import views

urlpatterns = [
    path(r'api-token-auth/', ObtainAuthToken.as_view(serializer_class=CustomJWTSerializer)),
    path(r'register/', views.RegisterView.as_view()),
    re_path(r'content/(?P<slug>[\w-]+)/$', views.ContentView.as_view()),
    re_path(r'friend/(?P<username>[\w-]+)/$', views.FriendsView.as_view()),
    re_path(r'rate/(?P<slug>[\w-]+)/$', views.RateView.as_view()),
    re_path(r'comments/(?P<slug>[\w-]+)/$', views.CommentView.as_view()),
    re_path(r'(?P<username>[\w-]+)/$', views.UserView.as_view(), name='user-info'),
]