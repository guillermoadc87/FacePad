from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer
from .models import User, Profile, Token

# Create your views here.
@api_view(['POST'])
def register(request):
    print(request.data)
    serializeduser = UserSerializer(data=request.data)
    serializedprofile = ProfileSerializer(data=request.data)
    if serializeduser.is_valid() and serializedprofile.is_valid():
        user = User.objects.create_user(
            email=serializeduser.data['email'],
            username=serializeduser.data['username'],
            password=serializeduser.data['password'],
            first_name=serializeduser.data['first_name'],
            last_name=serializeduser.data['last_name']
        )
        profile = Profile.get_or_create(user=user, date_of_birth=serializedprofile.data['date_of_birth'])
        profile.save()
        token = Token.objects.get_or_create(user=user)
        token.save()
        return Response(token.key, status=status.HTTP_201_CREATED)
    else:
        return Response(serializeduser._errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def example_view(request, format=None):
    print(request.user)
    return Response({'asd': 'asd'})