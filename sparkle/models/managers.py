from django.db import models
from .query import VersionQuerySet


class VersionManager(models.Manager):

    use_for_related_fields = True

    def get_queryset(self):
        return VersionQuerySet(self.model, using=self._db)

    def active(self, channel=None):
        return self.get_queryset().active(channel=channel)
