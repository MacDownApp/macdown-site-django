from django.utils.timezone import now
from django.db.models.query import QuerySet


class VersionQuerySet(QuerySet):
    def active(self, channel=None):
        qs = self.filter(publish_at__lte=now())
        if channel is None:
            return qs
        return qs.filter(channels__in=[channel])
