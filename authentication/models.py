from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # optional
    profile_photo = models.ImageField(verbose_name='photo de profil')
