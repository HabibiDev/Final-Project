from .models import Post, ImagePost, Category
from rest_framework import generics, renderers, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from django.contrib.auth.models import User
from .permissions import IsAuthorOrReadOnly, IsAuthorImageOrReadOnly
from django_filters import rest_framework as filters
import django_filters
from .serializers import (UserSerializer,
                          CategorySerializer,
                          ImagePostSerializer,
                          PostSerializer)


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
                          


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          permissions.IsAdminUser)


class ImageFilter(filters.FilterSet):
    class Meta:
        model = ImagePost
        fields = ['post_image', ]


class ImagePostViewSet(viewsets.ModelViewSet):

    queryset = ImagePost.objects.all()
    serializer_class = ImagePostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorImageOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ImageFilter


class PostFilter(filters.FilterSet):
    price = django_filters.RangeFilter('price')
    category = filters.ModelChoiceFilter(
        queryset=Category.objects.all(), method='category_filter')

    class Meta:
        model = Post
        fields = ['category', 'price']

    def category_filter(self, queryset, name, value):
        queryset = value.posts()
        return queryset


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(is_active=True).order_by('-updated')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
