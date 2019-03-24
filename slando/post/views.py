from .models import Post, ImagePost, Category
from rest_framework import generics, renderers, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from django.contrib.auth.models import User
from .permissions import IsAuthorOrReadOnly, IsUserOrReadOnly, IsAuthorImageOrReadOnly
from django_filters import rest_framework as filters
from mptt.fields import TreeNodeChoiceField, TreeNodeMultipleChoiceField
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
    #min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    #max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    price = filters.RangeFilter()

    class Meta:
        model = Post
        fields = ['category', 'price']


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.filter(is_active=True).order_by('title')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    def get_queryset(self, request):
        if request.data['category']:
            cat = Category.objects.get(name=request.data['category'])
