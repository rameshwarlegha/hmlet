from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'Tags'

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    owner = models.ForeignKey(User, related_name='posts',
                              on_delete=models.PROTECT)
    image = models.ImageField()
    caption = models.TextField()
    is_draft = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='total_posts')

    class Meta:
        db_table = 'Posts'
        ordering = ('-published_at',)

    def __str__(self):
        return self.caption

    @property
    def resized_image(self):
        image_original_url = self.image.url
        resized_url = image_original_url.replace(
            settings.AWS_STORAGE_BUCKET_NAME,
            settings.AWS_STORAGE_RESIZED_BUCKET_NAME)
        return resized_url
