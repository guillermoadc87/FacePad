
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate
from .models import User, Content, Rate, Comment
from django.utils.translation import ugettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
    birthday = serializers.DateTimeField()

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            birthday=validated_data['birthday'],

        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'birthday')
        write_only_fields = ('password',)

class ContentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    slug = serializers.CharField(required=False)

    class Meta:
        model = Content
        fields = ('title', 'slug', 'description', 'user', 'file')

    def create(self, validated_data):
        print(validated_data)
        data = validated_data.copy()
        data['user'] = self.context['request'].user

        return super(ContentSerializer, self).create(data)

    def validate_user(self, value):
        print(value)
        return value


class RateSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Rate
        fields = ('value', 'user')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ('text', 'user')

class CustomJWTSerializer(AuthTokenSerializer):
    username_field = 'username_or_email'

    def validate(self, attrs):
        password = attrs.get("password")

        user_obj = User.objects.filter(email=attrs.get("username")).first() or User.objects.filter(username=attrs.get("username")).first()

        if user_obj is not None:
            credentials = {
                'username': user_obj.username,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    if not user.is_active:
                        msg = _('User account is disabled.')
                        raise serializers.ValidationError(msg)

                    return {
                        'token': user.auth_token.key,
                        'user': user
                    }
                else:
                    msg = _('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg)

            else:
                msg = _('Must include "{username_field}" and "password".')
                msg = msg.format(username_field=self.username_field)
                raise serializers.ValidationError(msg)

        else:
            msg = _('Account with this email/username does not exists')
            raise serializers.ValidationError(msg)