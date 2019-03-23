from .models import Post, ImagePost, Category
from django.contrib.auth.models import User
from .serializers import UserSerializer, CategorySerializer, ImagePostSerializer, PostSerializer
from rest_framework import generics, renderers, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework import mixins
from .permissions import IsAuthorOrReadOnly, IsUserOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from mptt.fields import TreeNodeChoiceField, TreeNodeMultipleChoiceField


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsUserOrReadOnly,)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (permissions.AllowAny,)

        return super(UserViewSet, self).get_permissions()


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ImagePostListView(generics.ListCreateAPIView):

    queryset = ImagePost.objects.all()
    serializer_class = ImagePostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        image = ImagePost.objects.create(image=file)
        return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)


class PostFilter(filters.FilterSet):
    #min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    #max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    price = filters.RangeFilter()
    category = TreeNodeChoiceField()

    class Meta:
        model = Post
        fields = ['category', 'price']


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.filter(is_active=True)
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self, request)
    if request.data['category']:
        cat = Category.objects.get(name=request.data['category'])
