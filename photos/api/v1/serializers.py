from django.utils import timezone
from rest_framework.serializers import ModelSerializer

from photos.helpers import extract_hashtag
from photos.models import Post, Tag


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('image', 'caption', 'is_draft')

    def save(self, *args, **kwargs):
        post = Post(image=self.validated_data['image'],
                    caption=self.validated_data['caption'],
                    owner=kwargs.get('owner')
                    )

        if not self.validated_data['is_draft']:
            post.published_at = timezone.now()
        post.save()

        hash_tags = extract_hashtag(self.validated_data['caption'])
        for hash_tag in hash_tags:
            tag, created = Tag.objects.get_or_create(name=hash_tag)
            post.tags.add(tag)

        return post


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
        read_only_fields = ('id', 'resized_image', 'owner', 'published_at')

    def update(self, instance, validated_data):
        """
        """
        if instance.is_draft and not validated_data.get('is_draft', True):
            instance.is_draft = False
            instance.published_at = timezone.now()
        instance.caption = validated_data.get('caption', instance.caption)
        instance.save()

        if 'caption' in self.validated_data.keys():
            hash_tags = extract_hashtag(self.validated_data['caption'])
            tag_list = list()
            for hash_tag in hash_tags:
                tag, created = Tag.objects.get_or_create(name=hash_tag)
                tag_list.append(tag)
            instance.tags.set(tag_list)

        return instance
