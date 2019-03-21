from django.db import models
from django.contrib.auth.models import User
from post.models import Post


class UserAccount(User):
    favorites = models.ManyToManyField(Post)
