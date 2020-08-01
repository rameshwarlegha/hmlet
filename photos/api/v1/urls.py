from django.urls import path

from .views import PostCreateAPIView, PostListAPIView, PostUpdateDestroyAPIView

urlpatterns = [
    path('create', PostCreateAPIView.as_view()),
    path('', PostListAPIView.as_view()),
    path('<int:pk>/', PostUpdateDestroyAPIView.as_view()),
]
