from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from photos.api.v1.serializers import PostCreateSerializer, PostListSerializer, \
    PostDetailUpdateSerializer
from photos.models import Post

EARLIEST_PUBLISHED_DATE_SORT = 'ASC'


class PostCreateAPIView(CreateAPIView):
    """
    """
    serializer_class = PostCreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=self.request.user)
            return Response(status=status.HTTP_201_CREATED)


class PostListAPIView(ListAPIView):
    """
    """
    model = Post
    serializer_class = PostListSerializer

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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data,
                                           partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
