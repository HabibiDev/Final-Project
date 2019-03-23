from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (PostViewSet,
                    ImagePostListView,
                    CategoryListView,
                    UserViewSet)

app_name = 'post'

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('images', ImagePostListView.as_view(), name='images'),
    path('categories', CategoryListView.as_view(), name='categories'),


] + router.urls
