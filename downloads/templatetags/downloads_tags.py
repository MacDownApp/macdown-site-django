from django.core.urlresolvers import reverse
from django.template import Library

register = Library()


@register.simple_tag
def download_link(version):
    if version.short_version:
        return reverse('downloads:version', kwargs={
            'version': version.short_version
        })
    return version.update_url
