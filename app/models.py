from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)

class Book(models.Model):
    bookId = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    thumbnail = models.CharField(max_length=1000)

class Post(models.Model):
    postTitle = models.CharField(max_length=100)
    postText = models.CharField(max_length=100)
    bookId = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)