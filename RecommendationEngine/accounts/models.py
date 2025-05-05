from django.contrib.auth.models import AbstractUser, User
from django.db import models
import json

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

    blockedDevs = models.TextField(default="[]")  # JSON string (list of dev IDs)
    followedDevs = models.TextField(default="[]")
    blockedGames = models.TextField(default="[]")
    followedGames = models.TextField(default="[]")

    def get_blocked_devs(self):
        return json.loads(self.blockedDevs)

    def get_followed_games(self):
        return json.loads(self.followedGames)
    
class Developer(models.Model):
    devName = models.CharField(max_length=100, unique=True)

class Game(models.Model):
    gameName = models.CharField(max_length=255)
    genres = models.TextField(default="[]")  # JSON string for multiple genres
    dev = models.ForeignKey(Developer, on_delete=models.CASCADE)
    gameImage = models.TextField(default="placeholder")

class News(models.Model):
    newsTitle = models.CharField(max_length=255)
    newsContent = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)