from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token


class Category(MPTTModel):
    name = models.CharField(max_length=80, unique=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def posts(self):
        return Post.objects.filter(category=self.id)

    def __str__(self):
        return self.name


class ImagePost(models.Model):
    image_file = models.ImageField(
        upload_to='article/%Y/%m/%d', null=True, blank=True)
    post_image = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, blank=True)
    uploaded = models.DateTimeField(auto_now=True)


class Post(models.Model):
    title = models.CharField(max_length=100, unique=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    category = TreeForeignKey(
        Category, on_delete=models.CASCADE, related_name='posts_category')
    content = models.TextField(max_length=5000, null=True, blank=True)
    price = models.FloatField()
    contract_price = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def images(self):
        return ImagePost.objects.filter(post_image=self.id)

    def __str__(self):
        return self.title

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

