from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Post(TimeStampedModel):
    owner = models.ForeignKey(User, related_name='posts',
                              on_delete=models.PROTECT)
    image = models.ImageField()
    caption = models.TextField()
    is_draft = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'Posts'
        ordering = ('-published_at', )

    def __str__(self):
        return self.caption
