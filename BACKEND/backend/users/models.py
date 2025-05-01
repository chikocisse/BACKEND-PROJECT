
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Exemple pour 'groups'
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='users_customuser_set',  # unique related_name pour users
        blank=True
    )

    # Exemple pour 'user_permissions'
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='users_customuser_permissions_set',  # unique related_name pour users
        blank=True
    )
