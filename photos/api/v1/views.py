from rest_framework import status
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from photos.api.v1.serializers import PostCreateSerializer, PostListSerializer
from photos.models import Post


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=self.request.user)
            return Response(status=status.HTTP_201_CREATED)


class PostListAPIView(ListAPIView):
    model = Post
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)
