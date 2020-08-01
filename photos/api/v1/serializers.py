from django.utils import timezone
from rest_framework.serializers import ModelSerializer

from photos.models import Post


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('image', 'caption', 'is_draft')

    def save(self, *args, **kwargs):
        is_draft = self.validated_data['is_draft']
        post = Post(image=self.validated_data['image'],
                    caption=self.validated_data['caption'],
                    is_draft=self.validated_data['is_draft'],
                    owner=kwargs.get('owner')
                    )
        if not is_draft:
            post.published_at = timezone.now()
        post.save()


class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'owner', 'resized_image', 'caption', 'published_at',
                  'is_draft')


class PostDetailUpdateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'owner', 'resized_image', 'caption', 'published_at',
                  'is_draft')
        read_only_fields = ('id', 'resized_image', 'owner', 'published_at',
                            'is_draft')
