from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
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
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'owner', 'image', 'caption', 'published_at',
                  'is_draft')

    def get_image(self, obj):
        image_original_url = obj.image.url
        resized_url = image_original_url.replace(
            settings.AWS_STORAGE_BUCKET_NAME,
            settings.AWS_STORAGE_RESIZED_BUCKET_NAME)
        return resized_url
