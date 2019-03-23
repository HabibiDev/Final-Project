from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User


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
    uploaded = models.DateTimeField(auto_now=True)


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    category = TreeForeignKey(
        Category, on_delete=models.CASCADE, related_name='posts_category')
    content = models.TextField(max_length=5000, null=True, blank=True)
    image = models.ManyToManyField(ImagePost, related_name='posts_photo')
    price = models.FloatField()
    contract_price = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
