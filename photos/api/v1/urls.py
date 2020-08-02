from django.urls import path

from .views import (
    PostCreateAPIView, PostListAPIView,
    PostUpdateDestroyAPIView, PostBulKUpdateDeleteAPIVIew)

urlpatterns = [
    path('create/', PostCreateAPIView.as_view(), name='post_create'),
    path('', PostListAPIView.as_view(), name='post_list'),
    path('<int:pk>/', PostUpdateDestroyAPIView.as_view(),
         name='post_update_delete'),
    path('bulk-update-delete/', PostBulKUpdateDeleteAPIVIew.as_view(),
         name='post_bulk_update_delete')
]
