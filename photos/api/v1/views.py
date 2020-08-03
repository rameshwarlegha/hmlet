from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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
    """Publish a Post with Caption and draft functionality.
    """
    serializer_class = PostListCreateSerializer
    permission_classes = (IsAuthenticated,)

    post_create_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                      required=['image', 'caption',
                                                'is_draft'],
                                      properties={
                                          'caption': openapi.Schema(
                                              type=openapi.TYPE_STRING,
                                              title='Caption',
                                              description='Caption for the posts'),
                                          'image': openapi.Schema(
                                              type=openapi.TYPE_FILE,
                                              title='Image',
                                              description='Post Image'),
                                          'is_draft': openapi.Schema(
                                              type=openapi.TYPE_BOOLEAN,
                                              title='is_draft',
                                              description='Post is a draft or not.')})

    @swagger_auto_schema(request_body=post_create_body)
    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostListAPIView(ListAPIView):
    """Gets List of all Posts. Filter on #tags through query parameter.

    :param str tags: In Query parameters
    :param str sort_type: 'ASC'
    """
    model = Post
    serializer_class = PostListCreateSerializer
    posts_response = openapi.Response('Post List Response',
                                      PostListCreateSerializer)
    tags_parameter = openapi.Parameter(
        name='tags',
        in_=openapi.IN_QUERY,
        description='filter on #tags',
        type=openapi.TYPE_STRING,
        required=False)

    sort_parameter = openapi.Parameter(
        name='sort_type',
        in_=openapi.IN_QUERY,
        description='Sorting on Published Date',
        type=openapi.TYPE_STRING,
        required=False)

    @swagger_auto_schema(manual_parameters=[tags_parameter, sort_parameter],
                         responses={'200': [posts_response]})
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
    """API to Update and Delete a Single Post.
    """
    model = Post
    serializer_class = PostDetailUpdateSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user,
                                         id=self.kwargs.get('pk'))

    @swagger_auto_schema(auto_schema=None)
    def patch(self, request, *args, **kwargs):
        raise NotImplementedError


class PostBulKUpdateDeleteAPIVIew(RetrieveUpdateDestroyAPIView):
    """API for Bulk Updating, deleting of Posts by a User.
    """
    model = Post
    serializer_class = PostDetailUpdateSerializer
    permission_classes = (IsAuthenticated,)
    get_update_response = openapi.Response('Post Bulk Response',
                                           PostDetailUpdateSerializer)

    post_delete_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                      required=['ids', ],
                                      properties={
                                          'ids': openapi.Schema(
                                              type=openapi.TYPE_ARRAY,
                                              items=openapi.Schema(
                                                  type=openapi.TYPE_INTEGER),
                                              title='Ids',
                                              description='Id of the posts')})

    @swagger_auto_schema(responses={'200': [get_update_response]})
    def get_queryset(self, ids=None):
        queryset = self.model.objects.filter(owner=self.request.user)
        if ids:
            queryset = queryset.filter(id__in=ids)
        return queryset

    @swagger_auto_schema(responses={'200': [get_update_response]})
    def update(self, request, *args, **kwargs):
        ids = validate_ids(request.data)
        instances = self.get_queryset(ids=ids)
        serializer = self.get_serializer(
            instances, data=request.data, partial=True, many=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=post_delete_body)
    def delete(self, request, *args, **kwargs):
        ids = request.data.get('ids')
        instances = self.get_queryset(ids=ids)
        for instance in instances:
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(auto_schema=None)
    def patch(self, request, *args, **kwargs):
        raise NotImplementedError
