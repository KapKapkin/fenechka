import uuid

from django.db import models
from django.core import serializers
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        _('id'), 
        primary_key=True, 
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    username = models.CharField(_('username'), max_length=150, blank=True, unique=True, null=True)

    name = models.CharField(_('Name'), max_length=150)
    email = models.CharField(_('Email'), max_length=255, unique=True)

    town = models.CharField(verbose_name="Town/City",max_length=100, null=True, blank=True)
    about_me = models.CharField(_('About Me'), max_length=300, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png')

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    objects = CustomUserManager()

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='id_index')
        ]

    def toJSON(self):
        serialized_obj = serializers.serialize('json', [self, ], fields=['id', 'name', 'email', 'address', 'town', 'county',])
        return serialized_obj


class CustomUserManager(models.Model):
    def get_all(self):
        qs = CustomUser.objects.all()
        return qs

