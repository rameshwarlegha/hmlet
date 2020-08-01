from django.urls import path
from .views import PostCreateAPIView, PostListAPIView

urlpatterns = [
    path('create/', PostCreateAPIView.as_view()),
    path('', PostListAPIView.as_view()),
]
