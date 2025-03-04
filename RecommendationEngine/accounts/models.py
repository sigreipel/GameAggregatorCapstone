from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure uniqueness
    USERNAME_FIELD = 'email'  # Use email as the login field
    REQUIRED_FIELDS = ['username']  # Keep username for compatibility

        # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
    )