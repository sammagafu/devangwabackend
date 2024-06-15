# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_resized import ResizedImageField


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    profile = ResizedImageField(size=[100, 150], crop=['middle', 'center'], upload_to='profile')
    # is_kyc_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
