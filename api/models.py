from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Profile(models.Model):
    date_of_birth = models.Model('Date of Birth')
    friends = models.ManyToManyField(User)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)
    instance.profile.save()

# Create your models here.
class Content(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now())

class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    value = models.IntegerField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    created = models.DateTimeField(default=timezone.now())
    parent_comment = models.ForeignKey('Comment', on_delete=models.CASCADE)