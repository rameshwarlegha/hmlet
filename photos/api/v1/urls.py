from django.urls import path

from .views import (
    PostCreateAPIView, PostListAPIView,
    PostUpdateDestroyAPIView, PostBulKUpdateDeleteAPIVIew)

urlpatterns = [
    path('create/', PostCreateAPIView.as_view(), name='post-create'),
    path('', PostListAPIView.as_view(), name='post-list'),
    path('<int:pk>/', PostUpdateDestroyAPIView.as_view(),
         name='post-update-delete'),
    path('bulk-update-delete/', PostBulKUpdateDeleteAPIVIew.as_view(),
         name='post-bulk-update-delete')
]
