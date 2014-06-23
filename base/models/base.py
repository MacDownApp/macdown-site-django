from django.core.urlresolvers import reverse
from sparkle.models import Version
from .managers import MacDownVersionManager


class MacDownVersion(Version):

    objects = MacDownVersionManager()

    class Meta:
        proxy = True

    def get_absolute_url(self):
        return reverse('downloads:version', kwargs={
            'version': self.short_version,
        })
