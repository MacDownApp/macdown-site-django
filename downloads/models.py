from django.core.urlresolvers import reverse
from sparkle.models import Version


def version_get_absolute_url(obj):
    if obj.short_version:
        return reverse('downloads:short_version', kwargs={
            'short_version': obj.short_version
        })
    else:
        return reverse('downloads:version', kwargs={'version': obj.version})

Version.get_absolute_url = version_get_absolute_url
