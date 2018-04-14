from django.utils import timezone
from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.template.defaultfilters import slugify
from django.conf import settings

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=30, unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    birthday = models.DateTimeField(_('birthday'))
    is_active = models.BooleanField(_('active'), default=True)
    friends = models.ManyToManyField('User')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthday']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.user.username, filename)

# Create your models here.
class Content(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(_('slug'), max_length=60, unique=True)
    description = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now())

    def save(self, *args, **kwargs):
        if not self.id:
            # Only set the slug when the object is created.
            self.slug = slugify(self.title)  # Or whatever you want the slug to use
        super(Content, self).save(*args, **kwargs)

    def __str__(self):
        return "%s: %s" % (self.title, self.description)

class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now())
    value = models.IntegerField()

    def __str__(self):
        return str(self.value)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    created = models.DateTimeField(default=timezone.now())
    parent_comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.text