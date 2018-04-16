from dateutil.parser import parse
from rest_framework import permissions, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer, ContentSerializer, RateSerializer, CommentSerializer
from .models import User, Content

# Create your views here.
class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data.copy()

        if data.get('birthday'):
            data['birthday'] = parse(data.get('birthday'))

        serialized = UserSerializer(data=data)
        serialized.is_valid(raise_exception=True)
        user = serialized.save()
        return Response({'token': user.auth_token.key}, status=status.HTTP_201_CREATED)

class ContentView(APIView):

    def get(self, request, slug):
        try:
            content = Content.objects.get(slug=slug)
        except Content.DoesNotExist:
            return Response({'message': 'Can not find content'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_superuser or request.user == content.user:
            serializer = ContentSerializer(content)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'message': 'You are not allowed to view that content'}, status=status.HTTP_201_CREATED)

class CreateContentView(CreateAPIView):
    serializer_class = ContentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FriendsView(APIView):

    def get(self, request, username):
        try:
            friend = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'message': 'Can not find user'}, status=status.HTTP_400_BAD_REQUEST)

        if friend in request.user.friends.all():
            serialized = ContentSerializer(friend.content_set.all(), many=True)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'This user is not your friend'}, status=status.HTTP_201_CREATED)

class UserView(APIView):

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'message': 'Can not find user'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_superuser or request.user == user or request.user in user.friends.all():
            serialized = UserSerializer(user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response({'message': 'The user was not found'}, status=status.HTTP_404_NOT_FOUND)

class RateView(APIView):

    def get(self, request, slug):
        try:
            content = Content.objects.get(slug=slug)
        except Content.DoesNotExist:
            return Response({'message': 'Can not find content'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_superuser or request.user == content.user or request.user in content.user.friends.all():
            serialized = RateSerializer(content.rate_set.all(), many=True)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response({'message': 'This user is not allowed to view the rates'}, status=status.HTTP_404_NOT_FOUND)

class CommentView(APIView):

    def get(self, request, slug):
        try:
            content = Content.objects.get(slug=slug)
        except Content.DoesNotExist:
            return Response({'message': 'Can not find content'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_superuser or request.user == content.user or request.user in content.user.friends.all():
            serialized = CommentSerializer(content.comment_set.all(), many=True)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response({'message': 'This user is not allowed to view comments'}, status=status.HTTP_404_NOT_FOUND)
