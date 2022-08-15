from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Create one to one realationship to the User model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

