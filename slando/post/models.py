from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=80, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class ImagePost(models.Model):
    image_file = models.ImageField(
        upload_to='article/%Y/%m/%d', null=True, blank=True)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ImagePost"
        verbose_name_plural = "ImagePosts"


class Post(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField(max_length=5000, null=True, blank=True)
    image = models.ManyToManyField(ImagePost, related_name='posts')
    price = models.FloatField()
    contract_price = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title
