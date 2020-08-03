from django.utils import timezone
from rest_framework.serializers import ModelSerializer, ListSerializer

from photos.helpers import extract_hashtag
from photos.models import Post, Tag


class PostListCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'image', 'caption', 'is_draft', 'resized_image',
                  'published_at')
        read_only_fields = ('published_at', 'resized_image', 'id')

    def create(self, validated_data):
        post = Post(image=validated_data['image'],
                    caption=validated_data['caption'],
                    owner=self.context['request'].user
                    )

        if not validated_data['is_draft']:
            post.published_at = timezone.now()
        post.save()

        hash_tags = extract_hashtag(validated_data['caption'])
        for hash_tag in hash_tags:
            tag, created = Tag.objects.get_or_create(name=hash_tag)
            post.tags.add(tag)
        return post


class UpdateListSerializer(ListSerializer):
    """
    """

    def update(self, instances, validated_data):
        instance_hash = {index: instance for index, instance in
                         enumerate(instances)}

        result = [
            self.child.update(instance_hash[index], attrs)
            for index, attrs in enumerate(validated_data)

        ]
        return result


class PostDetailUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'owner', 'resized_image', 'caption', 'published_at',
                  'is_draft')
        read_only_fields = ('id', 'resized_image', 'owner', 'published_at')
        list_serializer_class = UpdateListSerializer

    def update(self, instance, validated_data):
        """
        """
        if instance.is_draft and not validated_data.get('is_draft', True):
            instance.is_draft = False
            instance.published_at = timezone.now()
        instance.caption = validated_data.get('caption', instance.caption)
        instance.save()

        if 'caption' in validated_data.keys():
            hash_tags = extract_hashtag(validated_data['caption'])
            tag_list = list()
            for hash_tag in hash_tags:
                tag, created = Tag.objects.get_or_create(name=hash_tag)
                tag_list.append(tag)
            instance.tags.set(tag_list)

        return instance
