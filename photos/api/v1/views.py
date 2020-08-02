from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from photos.api.v1.serializers import PostDetailUpdateSerializer, \
    PostListCreateSerializer
from photos.helpers import validate_ids
from photos.models import Post

EARLIEST_PUBLISHED_DATE_SORT = 'ASC'


class PostCreateAPIView(CreateAPIView):
    """
    """
    serializer_class = PostListCreateSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostListAPIView(ListAPIView):
    """
    """
    model = Post
    serializer_class = PostListCreateSerializer

    def get_queryset(self):
        queryset = self.model.objects.all()
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(owner=user)

        tags = self.request.GET.get('tags')
        if tags:
            tag_list = tags.split(',')
            queryset = queryset.filter(tags__name__in=tag_list).distinct()

        sort_type = self.request.GET.get('sort_type')
        if sort_type and sort_type == EARLIEST_PUBLISHED_DATE_SORT:
            queryset = queryset.order_by('published_at', '-created')

        return queryset


class PostUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    """
    model = Post
    serializer_class = PostDetailUpdateSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user,
                                         id=self.kwargs.get('pk'))


class PostBulKUpdateDeleteAPIVIew(RetrieveUpdateDestroyAPIView):
    """
    """
    model = Post
    serializer_class = PostDetailUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, ids=None):
        queryset = self.model.objects.filter(owner=self.request.user)
        if ids:
            queryset = queryset.filter(id__in=ids)
        return queryset

    def update(self, request, *args, **kwargs):
        ids = validate_ids(request.data)
        instances = self.get_queryset(ids=ids)
        serializer = self.get_serializer(
            instances, data=request.data, partial=True, many=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        ids = request.data.get('ids')
        instances = self.get_queryset(ids=ids)
        for instance in instances:
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
