from .models import Category, ImagePost, Post
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from django.core.exceptions import ObjectDoesNotExist


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    subcategories = RecursiveField(source="children",
                                   many=True, required=False)
    parent = serializers.ReadOnlyField(source='parent.name')
    posts = serializers.ReadOnlyField(source='posts.title')

    class Meta:
        model = Category
        fields = ('id', 'parent', 'name', 'subcategories', 'posts')


class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ('id', 'image_file', 'uploaded')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = CategorySerializer()
    image = ImagePostSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'category', 'content', 'image',
                  'price', 'contract_price', 'created', 'updated', 'is_active')
