from django.utils.functional import SimpleLazyObject
from django.core.urlresolvers import reverse
from sparkle.models import Application, Channel


macdown = SimpleLazyObject(lambda: Application.objects.get(slug='macdown'))


def channel_get_absolute_url(obj):
    return reverse('history:channel', kwargs={'slug': obj.slug})

Channel.get_absolute_url = channel_get_absolute_url
