from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (PostViewSet,
                    ImagePostViewSet,
                    CategoryListView,
                    UserCreate)

app_name = 'post'

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('images', ImagePostViewSet)


urlpatterns = [
    path('categories', CategoryListView.as_view(), name='categories'),
    path('users', UserCreate.as_view(), name='users'),


] + router.urls
